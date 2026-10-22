
from pathlib import Path
import pandas as pd

# Locate the Kaggle dataset files
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "kaggle_data"

files = {
    "Job Postings": DATA_DIR / "job_postings.csv",
    "Job Skills": DATA_DIR / "job_skills.csv",
    "Job Summaries": DATA_DIR / "job_summary.csv",
}

for name, file_path in files.items():
    print(f"\n{'=' * 50}")
    print(name)
    print(f"{'=' * 50}")

    if not file_path.exists():
        print(f"File not found: {file_path}")
        continue

    df = pd.read_csv(file_path, low_memory=False)

    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nMissing values (top 10):")
    print(df.isna().sum().sort_values(ascending=False).head(10))

    if "job_link" in df.columns:
        print(f"\nDuplicate job links: {df['job_link'].duplicated().sum():,}")
        print(f"Unique job links: {df['job_link'].nunique():,}")

    print("\nSample records:")
    print(df.head(3).to_string(index=False))
    
# Inspect job types and job titles
postings_path = DATA_DIR / "job_postings.csv"
df = pd.read_csv(postings_path, low_memory=False)

print("\n===== JOB TYPES =====")
print(df["job_type"].value_counts(dropna=False).to_string())

print("\n===== TOP 25 JOB TITLES =====")
print(df["job_title"].value_counts().head(25).to_string())

print("\n===== JOB LEVELS =====")
print(df["job_level"].value_counts(dropna=False).to_string())

print("\n===== FIRST SEEN DATE RANGE =====")
df["first_seen"] = pd.to_datetime(df["first_seen"], errors="coerce")
print("Earliest:", df["first_seen"].min())
print("Latest:", df["first_seen"].max())


# Additional dataset inspection

postings_path = DATA_DIR / "job_postings.csv"
df = pd.read_csv(postings_path, low_memory=False)

print("\n===== JOB TYPES =====")
print(df["job_type"].value_counts(dropna=False))

print("\n===== TOP 25 JOB TITLES =====")
print(df["job_title"].value_counts().head(25))

print("\n===== JOB LEVELS =====")
print(df["job_level"].value_counts(dropna=False))

print("\n===== FIRST SEEN DATE RANGE =====")
df["first_seen"] = pd.to_datetime(df["first_seen"], errors="coerce")
print("Earliest:", df["first_seen"].min())
print("Latest:", df["first_seen"].max())


# Inspect remote job postings

remote_jobs = df[
    df["job_type"].astype(str).str.contains("remote", case=False, na=False)
]

print("\n===== REMOTE JOB POSTINGS =====")
print("Total remote jobs:", len(remote_jobs))

print("\nRemote job titles:")
print(remote_jobs["job_title"].value_counts())

print("\nRemote job locations:")
print(remote_jobs["job_location"].value_counts())

print("\nRemote job levels:")
print(remote_jobs["job_level"].value_counts(dropna=False))

print("\nRemote job samples:")
print(
    remote_jobs[
        ["job_title", "company", "job_location", "job_level", "first_seen"]
    ].head(20).to_string(index=False)
)


# Filter remote jobs relevant to data analytics and data science

keywords = [
    "data analyst",
    "data scientist",
    "data engineer",
    "machine learning",
    "business intelligence",
    "analytics engineer",
    "data analytics",
    "business analyst",
    "bi analyst",
    "ml engineer",
    "mlops engineer",
]

relevant_remote_jobs = remote_jobs[
    remote_jobs["job_title"].str.contains(
        "|".join(keywords),
        case=False,
        na=False
    )
]

print("\n===== RELEVANT REMOTE DATA JOBS =====")
print("Total relevant remote jobs:", len(relevant_remote_jobs))

print(
    relevant_remote_jobs[
        ["job_title", "company", "job_location", "job_level", "first_seen"]
    ].to_string(index=False)
)


# Find relevant data roles across all work arrangements

all_relevant_jobs = df[
    df["job_title"].str.contains(
        "|".join(keywords),
        case=False,
        na=False
    )
]

print("\n===== RELEVANT DATA JOBS — ALL WORK TYPES =====")
print("Total relevant jobs:", len(all_relevant_jobs))

print("\nWork type distribution:")
print(all_relevant_jobs["job_type"].value_counts(dropna=False))

print("\nTop 30 relevant job titles:")
print(all_relevant_jobs["job_title"].value_counts().head(30))



# Inspect skills for relevant data jobs

skills_path = DATA_DIR / "job_skills.csv"
skills_df = pd.read_csv(skills_path, low_memory=False)

relevant_links = set(all_relevant_jobs["job_link"])

relevant_skills = skills_df[
    skills_df["job_link"].isin(relevant_links)
]

print("\n===== RELEVANT JOB SKILLS =====")
print("Matching skill records:", len(relevant_skills))
print("Missing skills:", relevant_skills["job_skills"].isna().sum())

print("\nSample skill records:")
print(relevant_skills.head(10).to_string(index=False))


# Inspect skills specifically for Data Analyst roles

analyst_jobs = df[
    df["job_title"].str.contains(
        "data analyst",
        case=False,
        na=False
    )
]

analyst_links = set(analyst_jobs["job_link"])

analyst_skills = skills_df[
    skills_df["job_link"].isin(analyst_links)
]

print("\n===== DATA ANALYST SKILLS =====")
print("Data Analyst postings:", len(analyst_jobs))
print("Matching skill records:", len(analyst_skills))

print("\nSample Data Analyst skills:")
print(analyst_skills.head(10).to_string(index=False))


from collections import Counter

# Count skills across Data Analyst postings
skill_counts = Counter()

for skills in analyst_skills["job_skills"].dropna():
    for skill in skills.split(","):
        skill = skill.strip()
        if skill:
            skill_counts[skill.lower()] += 1

print("\n===== TOP 20 DATA ANALYST SKILLS =====")

for skill, count in skill_counts.most_common(20):
    print(f"{skill}: {count}")


# Save Data Analyst skill frequencies

reports_dir = PROJECT_ROOT / "reports"
reports_dir.mkdir(exist_ok=True)

skills_report = pd.DataFrame(
    skill_counts.most_common(),
    columns=["skill", "job_count"]
)

output_path = reports_dir / "data_analyst_skill_frequency.csv"
skills_report.to_csv(output_path, index=False)

print(f"\nSkill report saved to: {output_path}")
print(f"Total distinct skill labels: {len(skills_report)}")


# Verify the saved skill report

saved_report = pd.read_csv(
    PROJECT_ROOT / "reports" / "data_analyst_skill_frequency.csv"
)

print("\n===== SAVED SKILL REPORT — TOP 20 =====")
print(saved_report.head(20).to_string(index=False))

print("\nTotal rows in saved report:", len(saved_report))


# Standardize common skill-name variations

skill_aliases = {
    "communication skills": "communication",
    "problem-solving": "problem solving",
    "problem solving skills": "problem solving",
    "data analytics": "data analysis",
    "powerbi": "power bi",
    "ms excel": "excel",
    "microsoft excel": "excel",
    "machine-learning": "machine learning",
}

cleaned_skills = skills_report.copy()

cleaned_skills["skill"] = (
    cleaned_skills["skill"]
    .str.strip()
    .str.lower()
    .replace(skill_aliases)
)

cleaned_skills = (
    cleaned_skills
    .groupby("skill", as_index=False)["job_count"]
    .sum()
    .sort_values("job_count", ascending=False)
)

cleaned_path = reports_dir / "data_analyst_skill_frequency_cleaned.csv"
cleaned_skills.to_csv(cleaned_path, index=False)

print("\n===== CLEANED TOP 20 SKILLS =====")
print(cleaned_skills.head(20).to_string(index=False))
print(f"\nCleaned report saved to: {cleaned_path}")
print("Distinct labels before:", len(skills_report))
print("Distinct labels after:", len(cleaned_skills))


# Validate the cleaned skills report

check_report = pd.read_csv(
    PROJECT_ROOT / "reports" / "data_analyst_skill_frequency_cleaned.csv"
)

print("\n===== CLEANED REPORT VALIDATION =====")
print("Total skill labels:", len(check_report))
print("Duplicate skill names:", check_report["skill"].duplicated().sum())
print("Missing skill names:", check_report["skill"].isna().sum())

print("\nTop 10 cleaned skills:")
print(check_report.head(10).to_string(index=False))



import matplotlib.pyplot as plt

# Create a chart of the top 10 Data Analyst skills
top_10 = check_report.head(10).sort_values("job_count")

plt.figure(figsize=(10, 6))
plt.barh(top_10["skill"], top_10["job_count"])
plt.xlabel("Number of skill mentions")
plt.ylabel("Skill")
plt.title("Top 10 Skills in Data Analyst Job Postings")
plt.tight_layout()

chart_path = reports_dir / "top_10_data_analyst_skills.png"
plt.savefig(chart_path, dpi=150, bbox_inches="tight")
plt.close()

print(f"\nSkill chart saved to: {chart_path}")

