import pandas as pd
import numpy as np
from pathlib import Path

CLEANED_DIR = Path(r"C:\Facultate\ANUL3_SEM2\DL\Project\ETL\data\processed\cleaned")
OUTPUT_DIR  = Path(r"C:\Facultate\ANUL3_SEM2\DL\Project\ETL\data\processed\splits")

TRAIN_RATIO = 0.70
VAL_RATIO   = 0.15
# test = remaining 15%

RANDOM_SEED = 42


def split_source_ids(source_ids: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(RANDOM_SEED)
    ids = rng.permutation(source_ids)

    n = len(ids)
    n_train = int(n * TRAIN_RATIO)
    n_val   = int(n * VAL_RATIO)

    return ids[:n_train], ids[n_train:n_train + n_val], ids[n_train + n_val:]


def split() -> dict[str, pd.DataFrame]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    h = pd.read_csv(CLEANED_DIR / "corpus_h_clean.csv")
    m = pd.read_csv(CLEANED_DIR / "corpus_m_clean.csv")
    p = pd.read_csv(CLEANED_DIR / "corpus_p_clean.csv")

    # Split pe source_id-urile din H (referinta)
    all_ids = h["source_id"].unique()
    train_ids, val_ids, test_ids = split_source_ids(all_ids)

    print(f"Source IDs total: {len(all_ids):,}")
    print(f"  train: {len(train_ids):,} | val: {len(val_ids):,} | test: {len(test_ids):,}")

    splits = {}
    for corpus_name, df in [("h", h), ("m", m), ("p", p)]:
        for split_name, ids in [("train", train_ids), ("val", val_ids), ("test", test_ids)]:
            key = f"{corpus_name}_{split_name}"
            subset = df[df["source_id"].isin(ids)].reset_index(drop=True)
            splits[key] = subset
            out_path = OUTPUT_DIR / f"{key}.csv"
            subset.to_csv(out_path, index=False)
            print(f"  {key}: {len(subset):,} rows -> {out_path.name}")

    return splits


if __name__ == "__main__":
    split()
