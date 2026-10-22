
from pathlib import Path
from collections import Counter

import matplotlib.pyplot as plt
import pandas as pd


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "kaggle_data"
REPORTS_DIR = PROJECT_ROOT / "reports"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)

POSTINGS_PATH = DATA_DIR / "job_postings.csv"
SKILLS_PATH = DATA_DIR / "job_skills.csv"
SUMMARIES_PATH = DATA_DIR / "job_summaries.csv"


# ============================================================
# 2. INSPECT DATASET FILES
# ============================================================

files = {
    "Job Postings": POSTINGS_PATH,
    "Job Skills": SKILLS_PATH,
    "Job Summaries": SUMMARIES_PATH,
}

for name, file_path in files.items():
    print(f"\n{'=' * 60}")
    print(name)
    print("=" * 60)

    if not file_path.exists():
        print(f"File not found: {file_path}")
        continue

    file_df = pd.read_csv(file_path, low_memory=False)

    print(f"Rows: {len(file_df):,}")
    print(f"Columns: {len(file_df.columns)}")
    print("\nColumn names:")
    print(file_df.columns.tolist())

    print("\nMissing values (top 10):")
    print(file_df.isna().sum().sort_values(ascending=False).head(10))

    if "job_link" in file_df.columns:
        print(
            "\nDuplicate job links:",
            f"{file_df['job_link'].duplicated().sum():,}",
        )
        print(
            "Unique job links:",
            f"{file_df['job_link'].nunique():,}",
        )

    print("\nSample records:")
    print(file_df.head(3).to_string(index=False))


# ============================================================
# 3. LOAD JOB POSTINGS
# ============================================================

if not POSTINGS_PATH.exists():
    raise FileNotFoundError(f"Job postings file not found: {POSTINGS_PATH}")

df = pd.read_csv(POSTINGS_PATH, low_memory=False)

required_columns = {
    "job_link",
    "job_title",
    "company",
    "job_location",
    "job_level",
    "job_type",
    "first_seen",
}

missing_columns = required_columns.difference(df.columns)

if missing_columns:
    raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

df["first_seen"] = pd.to_datetime(df["first_seen"], errors="coerce")


# ============================================================
# 4. GENERAL JOB POSTING ANALYSIS
# ============================================================

print("\n===== JOB TYPES =====")
print(df["job_type"].value_counts(dropna=False).to_string())

print("\n===== TOP 25 JOB TITLES =====")
print(df["job_title"].value_counts().head(25).to_string())

print("\n===== JOB LEVELS =====")
print(df["job_level"].value_counts(dropna=False).to_string())

print("\n===== FIRST SEEN DATE RANGE =====")
print("Earliest:", df["first_seen"].min())
print("Latest:", df["first_seen"].max())


# ============================================================
# 5. INSPECT REMOTE JOBS
# ============================================================

remote_mask = (
    df["job_type"]
    .astype("string")
    .str.contains("remote", case=False, na=False)
)

remote_jobs = df[remote_mask].copy()

print("\n===== REMOTE JOB POSTINGS =====")
print("Total remote jobs:", len(remote_jobs))

print("\nRemote job titles:")
print(remote_jobs["job_title"].value_counts().to_string())

print("\nRemote job locations:")
print(remote_jobs["job_location"].value_counts().to_string())

print("\nRemote job levels:")
print(remote_jobs["job_level"].value_counts(dropna=False).to_string())

print("\nRemote job samples:")
print(
    remote_jobs[
        ["job_title", "company", "job_location", "job_level", "first_seen"]
    ].head(20).to_string(index=False)
)


# ============================================================
# 6. FILTER RELEVANT DATA-RELATED JOBS
# ============================================================

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

title_pattern = "|".join(keywords)

relevant_remote_jobs = remote_jobs[
    remote_jobs["job_title"].str.contains(
        title_pattern,
        case=False,
        na=False,
    )
].copy()

print("\n===== RELEVANT REMOTE DATA JOBS =====")
print("Total relevant remote jobs:", len(relevant_remote_jobs))

print(
    relevant_remote_jobs[
        ["job_title", "company", "job_location", "job_level", "first_seen"]
    ].to_string(index=False)
)

all_relevant_jobs = df[
    df["job_title"].str.contains(
        title_pattern,
        case=False,
        na=False,
    )
].copy()

print("\n===== RELEVANT DATA JOBS - ALL WORK TYPES =====")
print("Total relevant jobs:", len(all_relevant_jobs))

print("\nWork type distribution:")
print(all_relevant_jobs["job_type"].value_counts(dropna=False).to_string())

print("\nTop 30 relevant job titles:")
print(all_relevant_jobs["job_title"].value_counts().head(30).to_string())


# ============================================================
# 7. LOAD AND MATCH JOB SKILLS
# ============================================================

if not SKILLS_PATH.exists():
    raise FileNotFoundError(f"Job skills file not found: {SKILLS_PATH}")

skills_df = pd.read_csv(SKILLS_PATH, low_memory=False)

if not {"job_link", "job_skills"}.issubset(skills_df.columns):
    raise ValueError("The job skills file must contain job_link and job_skills.")

relevant_links = set(all_relevant_jobs["job_link"])

relevant_skills = skills_df[
    skills_df["job_link"].isin(relevant_links)
]

print("\n===== RELEVANT JOB SKILLS =====")
print("Matching skill records:", len(relevant_skills))
print("Missing skills:", relevant_skills["job_skills"].isna().sum())

print("\nSample skill records:")
print(relevant_skills.head(10).to_string(index=False))


# ============================================================
# 8. DATA ANALYST SKILLS ANALYSIS
# ============================================================

analyst_jobs = df[
    df["job_title"].str.contains(
        "data analyst",
        case=False,
        na=False,
    )
].copy()

analyst_links = set(analyst_jobs["job_link"])

analyst_skills = skills_df[
    skills_df["job_link"].isin(analyst_links)
]

print("\n===== DATA ANALYST SKILLS =====")
print("Data Analyst postings:", len(analyst_jobs))
print("Matching skill records:", len(analyst_skills))

print("\nSample Data Analyst skills:")
print(analyst_skills.head(10).to_string(index=False))


# ============================================================
# 9. COUNT SKILL MENTIONS
# ============================================================

skill_counts = Counter()

for skills in analyst_skills["job_skills"].dropna():
    for skill in skills.split(","):
        skill = skill.strip().lower()

        if skill:
            skill_counts[skill] += 1

print("\n===== TOP 20 DATA ANALYST SKILLS =====")

for skill, count in skill_counts.most_common(20):
    print(f"{skill}: {count}")


# ============================================================
# 10. SAVE ORIGINAL SKILL FREQUENCY REPORT
# ============================================================

skills_report = pd.DataFrame(
    skill_counts.most_common(),
    columns=["skill", "job_count"],
)

original_report_path = REPORTS_DIR / "data_analyst_skill_frequency.csv"
skills_report.to_csv(original_report_path, index=False)

print(f"\nSkill report saved to: {original_report_path}")
print("Total distinct skill labels:", len(skills_report))


# ============================================================
# 11. STANDARDIZE COMMON SKILL NAME VARIATIONS
# ============================================================

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
    .reset_index(drop=True)
)

cleaned_report_path = (
    REPORTS_DIR / "data_analyst_skill_frequency_cleaned.csv"
)

cleaned_skills.to_csv(cleaned_report_path, index=False)

print("\n===== CLEANED TOP 20 SKILLS =====")
print(cleaned_skills.head(20).to_string(index=False))

print(f"\nCleaned report saved to: {cleaned_report_path}")
print("Distinct labels before:", len(skills_report))
print("Distinct labels after:", len(cleaned_skills))


# ============================================================
# 12. VALIDATE CLEANED REPORT
# ============================================================

check_report = pd.read_csv(cleaned_report_path)

print("\n===== CLEANED REPORT VALIDATION =====")
print("Total skill labels:", len(check_report))
print("Duplicate skill names:", check_report["skill"].duplicated().sum())
print("Missing skill names:", check_report["skill"].isna().sum())

print("\nTop 10 cleaned skills:")
print(check_report.head(10).to_string(index=False))


# ============================================================
# 13. CREATE TOP 10 SKILLS CHART
# ============================================================

top_10 = check_report.head(10).sort_values("job_count")

plt.figure(figsize=(10, 6))
plt.barh(top_10["skill"], top_10["job_count"])
plt.xlabel("Number of skill mentions")
plt.ylabel("Skill")
plt.title("Top 10 Skills in Data Analyst Job Postings")
plt.tight_layout()

chart_path = REPORTS_DIR / "top_10_data_analyst_skills.png"

plt.savefig(chart_path, dpi=150, bbox_inches="tight")
plt.close()

print(f"\nSkill chart saved to: {chart_path}")
