
import pandas as pd
from pathlib import Path

# Find the project directory and working dataset
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "job_postings.csv"

df = pd.read_csv(DATA_FILE)
print("\nListings with missing skills:")
missing_skills = df[df["skills"].isna()]
print(missing_skills[["job_id", "job_title", "company"]])

print("=== JOB MARKET DATA QUALITY REPORT ===")
print(f"Total job listings: {len(df)}")

# 1. Check required fields
required_columns = [
    "job_id",
    "job_title",
    "company",
    "remote_status",
    "skills",
]

print("\n1. Missing required information:")
for column in required_columns:
    missing = df[column].isna().sum()
    print(f"{column}: {missing} missing")

# 2. Check duplicate job IDs
print("\n2. Duplicate job IDs:")
print(df["job_id"].duplicated().sum())

# 3. Check invalid experience ranges
df["experience_min"] = pd.to_numeric(
    df["experience_min"], errors="coerce"
)
df["experience_max"] = pd.to_numeric(
    df["experience_max"], errors="coerce"
)

invalid_experience = df[
    (df["experience_min"] < 0)
    | (df["experience_max"] < df["experience_min"])
]

print("\n3. Invalid experience ranges:")
print(len(invalid_experience))

# 4. Check missing salary information
salary_missing = df["salary_min"].isna().sum()

print("\n4. Listings without a minimum salary:")
print(salary_missing)

print("\nData quality check completed.")
