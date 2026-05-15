from torch.utils.data import DataLoader, Dataset
import torch

class TextDataset(Dataset):
    def __init__(self, texts):
        self.texts = texts

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        return self.texts[idx]

def predict_batch(texts: list[str], model, tokenizer, device, batch_size: int = 32):
    dataset = TextDataset(texts)
    loader = DataLoader(dataset, batch_size=batch_size)

    all_probs = []
    all_preds = []

    model.eval()
    with torch.no_grad():
        for batch in loader:
            inputs = tokenizer(
                batch,
                return_tensors="pt",
                truncation=True,
                max_length=512,
                padding=True
            ).to(device)

            outputs = model(**inputs)
            probs = torch.softmax(outputs.logits, dim=-1)
            preds = outputs.logits.argmax(dim=-1)

            all_probs.extend(probs[:, 1].cpu().numpy())  # prob of class 1 (ai)
            all_preds.extend(preds.cpu().numpy())

    return all_preds, all_probs