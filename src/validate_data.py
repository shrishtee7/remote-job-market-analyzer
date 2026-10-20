
import pandas as pd
from pathlib import Path

# Locate the project and CSV file
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "job_postings.csv"

# Check whether the file exists
if not DATA_FILE.exists():
    print("Error: CSV template not found.")
    raise SystemExit(1)

# Read the CSV file
df = pd.read_csv(DATA_FILE)

print("\n--- Remote Job Market Analyzer ---")
print("CSV file loaded successfully!")

print("\nDataset shape:")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

print("\nColumn names:")
print(df.columns.tolist())

# Check for missing column names
if df.columns.isnull().any() or any(
    not str(col).strip() for col in df.columns
):
    print("\nWarning: Some column names are empty.")

# Check for duplicate column names
if df.columns.duplicated().any():
    print("\nWarning: Duplicate column names detected.")

print("\nData validation completed.")
