# AI Text Detector on RAID Benchmark

A fine-tuned **RoBERTa-base** classifier that distinguishes human-written text from AI-generated text. The model was trained and evaluated against the [RAID benchmark](https://raid-bench.xyz/), a standardized leaderboard for AI-generated text detection.

---

## Project Overview

The project fine-tunes `roberta-base` (124M parameters, **full fine-tuning — all weights trainable**) for binary classification:

| Label | Class |
|-------|-------|
| `1`   | Human-written |
| `0`   | AI-generated (original or paraphrased) |

Two training experiments were conducted:
- **Exp 1** — Human + AI-original (baseline)
- **Exp 2** — Human + AI-original + AI-paraphrased (robustness)

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Model | `roberta-base` via HuggingFace Transformers |
| Training | PyTorch + `torch.amp` (mixed precision FP16) |
| Data | RAID dataset (parquet → CSV pipeline) |
| Preprocessing | pandas, scikit-learn |
| Evaluation | scikit-learn metrics (AUROC, F1, MCC, confusion matrix) |
| Benchmark | `raid-bench` Python package |
| Training infrastructure | **Kaggle Notebook — NVIDIA Tesla T4 GPU (16 GB VRAM)** |

---

## Training Infrastructure

Training was performed on **Kaggle** using a single **NVIDIA Tesla T4 GPU (16 GB VRAM)**:

- Mixed-precision training (`torch.amp.GradScaler`) to fit larger batches
- Batch size: 32 (train), 64 (eval)
- ~20 minutes per epoch
- Total training time: ~3 × 20 min = ~1 hour per experiment run

---

## ETL Pipeline

Raw data originates from the RAID dataset distributed as **Parquet files**. The pipeline proceeds in stages:

### 1. Extract
Raw `.parquet` files are read and split into three corpora:
- `corpus_h` — human-written texts
- `corpus_m` — AI-generated texts (no adversarial attack)
- `corpus_p` — AI-generated texts with **paraphrase attack**

### 2. Transform / Clean (`ETL/src/transform.py`)
Each corpus is cleaned by removing rows with:
- Control characters (`\x00–\x1f`)
- HTML tags
- LaTeX environments (`\begin{...}`)
- Emoji / Unicode symbols
- High special-character ratio (> 40% of text)
- Missing `generation`, `source_id`, or `domain` fields

Retained columns: `generation`, `source_id`, `domain`, `model`, `attack`.

### 4. Dataset Construction (`ETL/src/transform.py::build_datasets`)
Final datasets assembled:

| Dataset | Contents |
|---------|----------|
| `train_exp1` | H_train + M_train |
| `train_exp2` | H_train + M_train + P_train |
| `val` | H_val + M_val |
| `test_standard` | H_test + M_test |
| `test_paraphrase` | H_test + P_test |

### 5. Stratified Sampling (Kaggle notebook)
50,000 samples per class, stratified by `domain` (and `model` for AI corpora), ensuring balanced domain coverage across GPT-4, LLaMA, Mistral, MPT, Cohere, GPT-2/3 variants.

---

## Model Architecture

```
Input Text
    │
    ▼
RoBERTa Tokenizer (max_length=256, truncation, padding)
    │
    ▼
RoBERTa Encoder (12 layers, hidden_size=768, 12 attention heads)
    │
    ▼
[CLS] token representation
    │
    ▼
Classification Head: Linear(768→768) → Dropout → Linear(768→2)
    │
    ▼
Softmax → [P(AI), P(Human)]
```

**Total parameters: 124,647,170 — all trainable (full fine-tuning, no layer freezing)**

### Hyperparameters

| Parameter | Value |
|-----------|-------|
| Optimizer | AdamW |
| Learning rate | `1e-5` |
| Weight decay | `0.01` |
| Batch size | `32` |
| Epochs | `3` |
| LR scheduler | Linear with warmup |
| Warmup ratio | `6%` |
| Gradient clipping | `max_norm=1.0` |
| Precision | Mixed FP16 (`torch.amp`) |

---

## Results

Best model checkpoint selected by highest **AUROC** on the validation set.

### Training History

| Epoch | Train Loss | Val AUROC | Val AUPRC | Val MCC | Val F1 Macro | Val Accuracy |
|-------|-----------|-----------|-----------|---------|-------------|-------------|
| 1     | 0.0989    | 0.9984    | —         | —       | 0.9615      | 96.15%      |
| 2     | 0.0233    | 0.9991    | —         | —       | 0.9705      | 97.05%      |
| 3     | 0.0101    | **0.9993**| **0.9992**| **0.9391**| 0.9688   | **96.88%**  |

### Final Evaluation Metrics (Best Checkpoint — Epoch 3)

| Metric | Value | Description |
|--------|-------|-------------|
| **AUROC** | **0.9993** | Area Under ROC Curve (primary metric) |
| **AUPRC** | **0.9992** | Area Under Precision-Recall Curve |
| **MCC** | **0.9391** | Matthews Correlation Coefficient (most balanced) |
| F1 Macro | 0.9688 | Macro-averaged F1 |
| F1 Binary | 0.9678 | Binary F1 (human class) |
| Accuracy | 96.88% | Overall accuracy |
| Precision | 0.9973 | Of texts predicted human, 99.7% are actually human |
| Recall | 0.9400 | Of all human texts, 94.0% correctly identified |
| Specificity | 0.9975 | Of all AI texts, 99.75% correctly identified |

### Confusion Matrix (Validation Set — 4,000 samples)

```
                 Predicted AI    Predicted Human
Actual AI            1995               5        ← only 5 AI texts misclassified
Actual Human          120            1880        ← 120 human texts missed
```

- **False Positive Rate**: 0.25% (AI misclassified as human)
- **False Negative Rate**: 6.0% (human text missed)

The model is extremely precise at flagging AI text (99.7% precision) with a slight trade-off in recall for human texts.

---

## Installation

```bash
git clone https://github.com/Mosshato/AITextDetectorOnRAIDBenchmark.git
cd AITextDetectorOnRAIDBenchmark

python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS

pip install torch transformers pandas scikit-learn
```

---

## How to Run

### Run inference on custom text

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

model_dir = "ai-text-detector/model"
tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = AutoModelForSequenceClassification.from_pretrained(model_dir)
model.eval()

text = "Your text to classify here."
inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=256)
with torch.no_grad():
    logits = model(**inputs).logits
probs = torch.softmax(logits, dim=-1)
print(f"P(human): {probs[0][1]:.4f} | P(AI): {probs[0][0]:.4f}")
```

### Run the ETL pipeline

```bash
# Convert raw parquet corpora to CSV
python ETL/src/parquet_to_csv.py

# Split by source_id (70/15/15)
python ETL/src/split.py

# Build final labeled datasets
python ETL/src/transform.py

# Prepare balanced test dataset (AI vs Human)
python ai-text-detector/Tests/Data/utilsTestDataset.py
```

### Run training (Kaggle)

Open `ai-text-detector/Tests/trainrobertaaitextdetector.ipynb` in a Kaggle notebook with GPU (T4) accelerator enabled.

### Run evaluation on RAID benchmark

Open `ai-text-detector/Tests/testrobertamodel.ipynb` in a Kaggle notebook.

---

## Folder Structure

```
AITextDetectorOnRAIDBenchmark/
├── ai-text-detector/
│   ├── model/                          # Trained model weights & tokenizer
│   │   ├── config.json
│   │   ├── model.safetensors           # RoBERTa fine-tuned weights
│   │   ├── tokenizer.json
│   │   └── tokenizer_config.json
│   └── Tests/
│       ├── trainrobertaaitextdetector.ipynb   # Full training notebook (Kaggle/T4)
│       ├── testrobertamodel.ipynb             # RAID benchmark evaluation
│       ├── dataSetModel.py                    # Batched inference utility
│       ├── checkGPU.py                        # GPU availability check
│       ├── confusion_matrix.png               # Confusion matrix visualization
│       ├── predictions.json                   # RAID benchmark predictions
│       ├── Data/
│       │   ├── dataset.csv                    # Balanced test dataset (AI + Human)
│       │   └── utilsTestDataset.py            # Test dataset builder
│       ├── model/                             # Local model copy for testing
│       └── raid/                              # RAID benchmark submodule
├── ETL/
│   ├── run.py                                 # Pipeline entry point
│   ├── pipeline.txt                           # Pipeline documentation
│   └── src/
│       ├── parquet_to_csv.py                  # Convert parquet corpora to CSV
│       ├── transform.py                       # Data cleaning & dataset builder
│       ├── split.py                           # Source-ID-based train/val/test split
│       └── utils.py                           # Column distribution analysis
├── 2307.03838v2.pdf                           # RAID benchmark paper
├── .gitignore
└── README.md
```

---

## References

- RAID Benchmark: https://raid-bench.xyz/
- Base model: `roberta-base` (Liu et al., 2019)
- Model on HuggingFace: https://huggingface.co/Mosshato/ai-text-detector