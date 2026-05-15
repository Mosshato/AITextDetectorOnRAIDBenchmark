import re
import pandas as pd
from pathlib import Path

CORPS_DIR   = Path(r"C:\Facultate\ANUL3_SEM2\DL\Project\ETL\data\processed\corps")
CLEANED_DIR = Path(r"C:\Facultate\ANUL3_SEM2\DL\Project\ETL\data\processed\cleaned")
SPLITS_DIR  = Path(r"C:\Facultate\ANUL3_SEM2\DL\Project\ETL\data\processed\splits")
DATASETS_DIR = Path(r"C:\Facultate\ANUL3_SEM2\DL\Project\ETL\data\processed\datasets")

KEEP_COLS = ["generation", "source_id", "domain", "model", "attack"]

# Regex patterns for bias-inducing content
_RE_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
_RE_HTML_TAGS     = re.compile(r"<[a-zA-Z/][^>]{0,100}>")
_RE_LATEX_ENV     = re.compile(r"\\(begin|end)\{[^}]{1,50}\}")
_RE_EMOJI         = re.compile(r"[\U00010000-\U0010ffff]", flags=re.UNICODE)
_RE_SPECIAL_CHAR  = re.compile(r"[^a-zA-Z0-9\s]")

SYMBOL_RATIO_THRESHOLD = 0.4


def _has_control_chars(text: str) -> bool:
    return bool(_RE_CONTROL_CHARS.search(text))

def _has_html(text: str) -> bool:
    return bool(_RE_HTML_TAGS.search(text))

def _has_latex_env(text: str) -> bool:
    return bool(_RE_LATEX_ENV.search(text))

def _has_emoji(text: str) -> bool:
    return bool(_RE_EMOJI.search(text))

def _high_symbol_ratio(text: str) -> bool:
    if not text:
        return True
    special = len(_RE_SPECIAL_CHAR.findall(text))
    return (special / len(text)) > SYMBOL_RATIO_THRESHOLD

def _is_biased(text: str) -> bool:
    return (
        _has_control_chars(text)
        or _has_html(text)
        or _has_latex_env(text)
        or _has_emoji(text)
        or _high_symbol_ratio(text)
    )

def _clean_corpus(df: pd.DataFrame, corpus_name: str) -> pd.DataFrame:
    initial = len(df)

    if corpus_name == "h":
        df = df.copy()
        df["model"] = "human"  
        df["attack"] = "none"
    df = df[[c for c in KEEP_COLS if c in df.columns]]
    for col in KEEP_COLS:
        if col not in df.columns:
            df[col] = None
    df = df[KEEP_COLS]

    critical = ["generation", "source_id", "domain"]
    df = df.dropna(subset=critical)
    df = df[df["generation"].str.strip().ne("")]
    after_nan = len(df)

    mask_biased = df["generation"].apply(_is_biased)
    df = df[~mask_biased]
    
    return df.reset_index(drop=True)


# def transform() -> dict[str, pd.DataFrame]:
#     """Pasul 2 — curatare corpusuri (rulat deja)"""
#     CLEANED_DIR.mkdir(parents=True, exist_ok=True)
#     results = {}
#     for corpus_name in ["h", "m", "p"]:
#         path = CORPS_DIR / f"corpus_{corpus_name}.csv"
#         df = pd.read_csv(path)
#         df_clean = _clean_corpus(df, corpus_name)
#         out_path = CLEANED_DIR / f"corpus_{corpus_name}_clean.csv"
#         df_clean.to_csv(out_path, index=False)
#         results[corpus_name] = df_clean
#     return results


# ---------------------------------------------------------------------------
# Pasul 4 + 5 — Construire dataset final + Labeling
# ---------------------------------------------------------------------------

LABEL_MAP = {"h": 1, "m": 0, "p": 0}  # H=human, M/P=AI


def _load_split(corpus: str, split: str) -> pd.DataFrame:
    path = SPLITS_DIR / f"{corpus}_{split}.csv"
    df = pd.read_csv(path)
    df["label"] = LABEL_MAP[corpus]
    return df


def build_datasets() -> dict[str, pd.DataFrame]:
    DATASETS_DIR.mkdir(parents=True, exist_ok=True)

    h_train = _load_split("h", "train")
    m_train = _load_split("m", "train")
    p_train = _load_split("p", "train")

    h_val   = _load_split("h", "val")
    m_val   = _load_split("m", "val")

    h_test  = _load_split("h", "test")
    m_test  = _load_split("m", "test")
    p_test  = _load_split("p", "test")

    datasets = {
        # Experiment 1: baseline H + M
        "train_exp1": pd.concat([h_train, m_train], ignore_index=True),
        # Experiment 2: robust H + M + P
        "train_exp2": pd.concat([h_train, m_train, p_train], ignore_index=True),
        # Validare
        "val":        pd.concat([h_val, m_val], ignore_index=True),
        # Test standard: H vs M
        "test_standard":   pd.concat([h_test, m_test], ignore_index=True),
        # Test paraphrase: H vs P
        "test_paraphrase": pd.concat([h_test, p_test], ignore_index=True),
    }

    for name, df in datasets.items():
        out_path = DATASETS_DIR / f"{name}.csv"
        df.to_csv(out_path, index=False)
        n_human = (df["label"] == 1).sum()
        n_ai    = (df["label"] == 0).sum()
        print(f"[{name}] {len(df):>7,} rows | human={n_human:,} | AI={n_ai:,}")

    return datasets


if __name__ == "__main__":
    build_datasets()
