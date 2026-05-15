import pandas as pd
from pathlib import Path

CORPS_DIR = Path(r"C:\Facultate\ANUL3_SEM2\DL\Project\ETL\data\processed\corps")

def convert_parquet_to_csv(input_dir: Path = CORPS_DIR) -> None:
    parquet_files = list(input_dir.glob("*.parquet"))

    if not parquet_files:
        print(f"No parquet files found in {input_dir}")
        return

    for parquet_path in parquet_files:
        csv_path = parquet_path.with_suffix(".csv")
        df = pd.read_parquet(parquet_path)
        df.to_csv(csv_path, index=False)
        print(f"Converted: {parquet_path.name} -> {csv_path.name} ({len(df):,} rows)")

if __name__ == "__main__":
    convert_parquet_to_csv()
