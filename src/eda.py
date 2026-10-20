
import pandas as pd

# Load the job listings dataset
DATA_FILE = "data/job_postings.csv"
df = pd.read_csv(DATA_FILE)

# Display basic dataset information
print("=== REMOTE JOB MARKET ANALYZER ===")

print("\n1. Dataset dimensions:")
print(f"Total job listings: {df.shape[0]}")
print(f"Total columns: {df.shape[1]}")

print("\n2. Job titles:")
print(df["job_title"].value_counts().to_string())
# Visualize job-title distribution
import matplotlib.pyplot as plt

job_counts = df["job_title"].value_counts().sort_values()

plt.figure(figsize=(10, 6))
plt.barh(job_counts.index, job_counts.values)

plt.title("Job Title Distribution in Remote Job Listings")
plt.xlabel("Number of Job Listings")
plt.ylabel("Job Title")
plt.tight_layout()

plt.savefig("reports/job_title_distribution.png", dpi=300)
plt.show()

print("\nJob-title distribution chart saved successfully.")
print("\n3. Remote work status:")
print(df["remote_status"].value_counts().to_string())

print("\n4. Experience requirements:")
print(df[["job_id", "job_title", "experience_min", "experience_max"]].to_string(index=False))



# 5. Summary of experience requirements
print("\n5. Experience summary:")

valid_experience = df.dropna(
    subset=["experience_min", "experience_max"]
)

print(f"Listings with experience information: {len(valid_experience)}")
print(f"Average minimum experience: {valid_experience['experience_min'].mean():.1f} years")
print(f"Average maximum experience: {valid_experience['experience_max'].mean():.1f} years")
print(f"Entry-level listings (0 years minimum): {(valid_experience['experience_min'] == 0).sum()}")

# Visualize minimum experience requirements
import matplotlib.pyplot as plt

experience_counts = valid_experience["experience_min"].value_counts().sort_index()

plt.figure(figsize=(8, 5))
plt.bar(
    experience_counts.index.astype(str),
    experience_counts.values
)

plt.title("Minimum Experience Required for Remote Jobs")
plt.xlabel("Minimum Experience (Years)")
plt.ylabel("Number of Job Listings")
plt.tight_layout()

plt.savefig("reports/experience_requirements.png", dpi=300)
plt.show()

print("\nExperience requirements chart saved successfully.")


# 6. Most requested skills
print("\n6. Most requested skills:")

from collections import Counter

all_skills = []

for skill_list in df["skills"].dropna():
    skills = skill_list.split(";")
    for skill in skills:
        skill = skill.strip()
        if skill:
            all_skills.append(skill)

skill_counts = Counter(all_skills)

skills_df = pd.DataFrame(
    skill_counts.most_common(),
    columns=["Skill", "Job_Count"]
)

print(skills_df.to_string(index=False))

# Save skill frequency analysis to a CSV report
skills_df.to_csv(
    "reports/skills_frequency.csv",
    index=False
)

print("\nSkill frequency report saved successfully.")


# 7. Visualize the top 10 skills
import matplotlib.pyplot as plt

top_skills = skills_df.head(10).sort_values(
    by="Job_Count", ascending=True
)

plt.figure(figsize=(10, 6))
plt.barh(top_skills["Skill"], top_skills["Job_Count"])

plt.title("Top 10 Skills in Remote Job Listings")
plt.xlabel("Number of Job Listings")
plt.ylabel("Skill")
plt.tight_layout()

# Save chart for the project report
plt.savefig("reports/top_10_skills.png", dpi=300)
plt.show()

print("\nChart saved to reports/top_10_skills.png")
