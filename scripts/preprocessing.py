import os
import re
import pandas as pd
from collections import defaultdict
root_dir = "processing/output"
output_dir = "processing/combined"
os.makedirs(output_dir, exist_ok=True)



# Define sort order by event type
ascending_types = {"sprints", "middlelong", "hurdles", "relays", "road-running","race-walks"}
descending_types = {"throws", "jumps", "combined-events"}

track_types = {"sprints", "middlelong", "hurdles", "relays", "road-running", "race-walks"}
field_types = {"throws", "jumps"}
mixed_types = {"combined-events"} 


# Custom name normalization
manual_aliases = {
    "100m-hurdles": "100-metres-hurdles",
    "110m-hurdles": "110-metres-hurdles",
    "400m-hurdles": "400-metres-hurdles",
    "decathlon-u20": "decathlon",
    "decathlon-boys": "decathlon",
    "heptathlon-girls": "heptathlon",
}

def parse_mark(mark):
    mark = str(mark).strip().lower().replace("h", "")  # Strip 'h'
    try:
        if ":" in mark:
            minutes, seconds = mark.split(":")
            return int(minutes) * 60 + float(seconds)
        return float(mark)
    except:
        return float("inf")

def normalize_discipline(discipline_slug):
    # Apply exact manual alias first
    if discipline_slug in manual_aliases:
        return manual_aliases[discipline_slug]
    
    # Apply substring replacements from aliases
    for alias, standard in manual_aliases.items():
        if alias in discipline_slug:
            discipline_slug = discipline_slug.replace(alias, standard)
    
    # Remove trailing equipment/age specs (e.g., -990cm, -5kg, -u20, etc.)
    discipline_slug = re.sub(r"[-_](\d+(kg|g|cm)|u18|u20|senior|girls|boys)$", "", discipline_slug)

    return discipline_slug


def parse_mark_to_number(mark):
    mark = str(mark).strip().lower().replace("h", "")
    try:
        if ":" in mark:
            parts = mark.split(":")
            parts = [float(p) for p in parts]
            if len(parts) == 3:  # H:M:S
                return parts[0] * 3600 + parts[1] * 60 + parts[2]
            elif len(parts) == 2:  # M:S
                return parts[0] * 60 + parts[1]
            else:
                return float("inf")
        return float(mark)
    except:
        return float("inf")

def extract_country_code_from_venue(venue):
    match = re.search(r"\((\w{3})\)", str(venue))
    return match.group(1) if match else None

# Collect files
files_by_gender_and_discipline = defaultdict(list)

for gender in os.listdir(root_dir):
    gender_path = os.path.join(root_dir, gender)
    if not os.path.isdir(gender_path):
        continue
    for file in os.listdir(gender_path):
        if file.endswith(".csv"):
            parts = file.replace(".csv", "").split("_")
            if len(parts) >= 3:
                type_slug = parts[0]
                discipline_slug = "_".join(parts[1:-1])
                base_discipline = normalize_discipline(discipline_slug)
                key = (gender, type_slug, base_discipline)
                files_by_gender_and_discipline[key].append(os.path.join(gender_path, file))

# Combine and sort
for (gender, type_slug, discipline_key), file_list in files_by_gender_and_discipline.items():
    df = pd.concat([pd.read_csv(f) for f in file_list], ignore_index=True)

    df["normalized_discipline"] = discipline_key

    # Add track_field classification
    if type_slug in field_types:
        df["track_field"] = "field"
    elif type_slug in track_types:
        df["track_field"] = "track"
    elif type_slug in mixed_types:
        df["track_field"] = "mixed"
    else:
        df["track_field"] = "unknown"

    if "mark" not in df.columns:
        print(f" Skipping {discipline_key} — missing 'Mark'")
        continue

    df["Parsed Mark"] = df["mark"].apply(parse_mark)

    sort_ascending = type_slug in ascending_types

    # Apply numeric mark parsing (before sorting/ranking)
    df["mark_numeric"] = df["mark"].apply(parse_mark_to_number)
    df = df.sort_values("mark_numeric", ascending=sort_ascending).reset_index(drop=True)
    df["venue_country"] = df["venue"].apply(extract_country_code_from_venue)
    
    # Remove the helper column
    df.drop(columns=["Parsed Mark"], inplace=True)

    for col in ["dob", "date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format="%d %b %Y", errors="coerce")

    # Age in full years (always rounded down)
    if "dob" in df.columns and "date" in df.columns:
        df["age_at_event"] = (df["date"] - df["dob"]).dt.days // 365

    if "date" in df.columns:
        df["season"] = df["date"].dt.year

    output_path = os.path.join(output_dir, f"{gender}_{type_slug}_{discipline_key}.csv")
    df.to_csv(output_path, index=False)
    print(f" Saved sorted and ranked: {output_path}")
