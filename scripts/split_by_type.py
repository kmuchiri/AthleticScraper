import numpy as np
import pandas as pd
import os

# Load full dataset
df = pd.read_csv('datasets/all_disciplines_combined.csv')

# Separate relay and non-relay events
individual_df = df[df["type"] != "relays"]
relay_df = df[df["type"] == "relays"].drop(columns=["dob", "age_at_event"])

# Save global-level splits
individual_df.to_csv("datasets/individual_events.csv", index=False)
relay_df.to_csv("datasets/relay_events.csv", index=False)

# Split both datasets by gender
for gender in ["male", "female"]:
    gender_individual = individual_df[individual_df["sex"] == gender]
    gender_relay = relay_df[relay_df["sex"] == gender]

    # --- Split by type ---
    type_output_dir = f"datasets/split_by_type/{gender}"
    os.makedirs(type_output_dir, exist_ok=True)

    for event_type, df_group in gender_individual.groupby("type"):
        filename = f"{event_type}.csv"
        filepath = os.path.join(type_output_dir, filename)
        df_group.to_csv(filepath, index=False)
        print(f" Saved: {filepath}")

    # --- Split by discipline ---
    discipline_output_dir = f"datasets/split_by_discipline/{gender}"
    os.makedirs(discipline_output_dir, exist_ok=True)

    for discipline, df_group in gender_individual.groupby("normalized_discipline"):
        filename = f"{discipline}.csv"
        filepath = os.path.join(discipline_output_dir, filename)
        df_group.to_csv(filepath, index=False)
        print(f" Saved: {filepath}")
