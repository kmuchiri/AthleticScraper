import os
import pandas as pd

# folder directory containing all the combined csv files
combined_dir = "processing/combined"

# List all CSV files
csv_files = [f for f in os.listdir(combined_dir) if f.endswith(".csv")]

# Load and concatenate
all_dataframes = []
for file in csv_files:
    df = pd.read_csv(os.path.join(combined_dir, file))
    all_dataframes.append(df)

# Combine into a single DataFrame
combined_df = pd.concat(all_dataframes, ignore_index=True)

# Save to a new CSV
combined_df.to_csv("datasets/all_disciplines_combined.csv", index=False)
print("Combined CSV saved as 'all_disciplines_combined.csv'")

