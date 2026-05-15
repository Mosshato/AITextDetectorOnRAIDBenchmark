import pandas as pd

df = pd.read_parquet(r"C:\Facultate\ANUL3_SEM2\DL\Project\ETL\data\raw\train_clean.parquet")

relevant_cols = ['model', 'decoding', 'repetition_penalty', 'attack', 'domain']

for col in relevant_cols:
    print(f"\n{'='*50}")
    print(f"=== {col.upper()} ===")
    print(f"{'='*50}")
    counts = df[col].value_counts(dropna=False)
    pct = df[col].value_counts(dropna=False, normalize=True) * 100
    report = pd.DataFrame({'count': counts, 'percent': pct.round(2)})
    print(report.to_string())
    print(f"\nTotal non-null: {df[col].notna().sum()} / {len(df)}")

# distributie combinata model x domain (cea mai importanta pentru stratificare)
print(f"\n{'='*50}")
print("=== MODEL x DOMAIN (combined) ===")
print(f"{'='*50}")
cross = pd.crosstab(df['model'].fillna('human'), df['domain'], margins=True)
print(cross.to_string())

print(f"\nTotal dataset size: {len(df):,} rows")