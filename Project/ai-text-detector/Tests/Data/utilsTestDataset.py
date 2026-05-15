import pandas as pd
from sklearn.utils import shuffle
import os
# Load
ai_df = pd.read_csv("C:\Facultate\ANUL3_SEM2\DL\Project\ETL\data\processed\FINAL\m_test.csv")
human_df = pd.read_csv("C:\Facultate\ANUL3_SEM2\DL\Project\ETL\data\processed\FINAL\h_test.csv")

# Keep only the text column, add labels
ai_df = pd.DataFrame({"text": ai_df["generation"], "label": 0})
human_df = pd.DataFrame({"text": human_df["generation"], "label": 1})

# Balance: trim the larger to match the smaller
min_size = min(len(ai_df), len(human_df))
ai_df = ai_df.sample(n=min_size, random_state=42)
human_df = human_df.sample(n=min_size, random_state=42)

# Combine and shuffle
combined = pd.concat([ai_df, human_df], ignore_index=True)
combined = shuffle(combined, random_state=42).reset_index(drop=True)

# Save
combined.to_csv("dataset.csv", index=False)

print(f"Total rows: {len(combined)}")
print(combined["label"].value_counts())