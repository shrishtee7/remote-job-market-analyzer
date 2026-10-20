
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from pathlib import Path

# Configure the dashboard
st.set_page_config(
    page_title="Remote Job Market Analyzer",
    page_icon="📊",
    layout="wide"
)

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "job_postings.csv"

# Load job data
@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE)

df = load_data()

# Dashboard heading
st.title("📊 Remote Job Market Analyzer")
st.write(
    "Explore remote job listings, required skills, "
    "experience levels, and available salary information."
)

st.divider()

# Key metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Job Listings", len(df))

with col2:
    st.metric("Unique Job Titles", df["job_title"].nunique())

with col3:
    remote_count = (
        df["remote_status"].str.contains(
            "remote", case=False, na=False
        ).sum()
    )
    st.metric("Remote Listings", int(remote_count))

# Show the original job data

# Filter job listings by job title
st.subheader("Explore Job Listings")

job_titles = sorted(df["job_title"].dropna().unique())

selected_titles = st.multiselect(
    "Filter by Job Title",
    options=job_titles,
    default=job_titles
)

filtered_df = df[
    df["job_title"].isin(selected_titles)
]
filtered_df = df[
    df["job_title"].isin(selected_titles)
].copy()

# Filter by minimum years of experience
st.subheader("Filter by Experience")

experience_values = pd.to_numeric(
    df["experience_min"], errors="coerce"
).dropna()

if not experience_values.empty:
    min_exp = int(experience_values.min())
    max_exp = int(experience_values.max())

    selected_experience = st.slider(
        "Minimum experience required (years)",
        min_value=min_exp,
        max_value=max_exp,
        value=(min_exp, max_exp)
    )

    filtered_df = filtered_df[
        pd.to_numeric(
            filtered_df["experience_min"], errors="coerce"
        ).between(
            selected_experience[0],
            selected_experience[1]
        )
    ]


st.write(f"Showing {len(filtered_df)} job listings")

st.dataframe(filtered_df, use_container_width=True)

# Most requested skills
st.divider()
st.subheader("Most Requested Skills")

from collections import Counter

all_skills = []

for skill_list in filtered_df["skills"].dropna():
    for skill in skill_list.split(";"):
        skill = skill.strip()
        if skill:
            all_skills.append(skill)

skill_counts = Counter(all_skills)

if skill_counts:
    skills_df = pd.DataFrame(
        skill_counts.most_common(10),
        columns=["Skill", "Job_Count"]
    )

    skills_df = skills_df.sort_values(
        "Job_Count", ascending=True
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(skills_df["Skill"], skills_df["Job_Count"])

    ax.set_xlabel("Number of Job Listings")
    ax.set_ylabel("Skill")
    ax.set_title("Top 10 Skills in Selected Listings")

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
else:
    st.info("No skills available for the selected listings.")

# Salary analysis
st.divider()
st.subheader("Salary Analysis")

salary_df = filtered_df.dropna(
    subset=["salary_min", "salary_max"]
).copy()

if not salary_df.empty:
    salary_df["salary_min"] = pd.to_numeric(
        salary_df["salary_min"], errors="coerce"
    )
    salary_df["salary_max"] = pd.to_numeric(
        salary_df["salary_max"], errors="coerce"
    )

    salary_df = salary_df.dropna(
        subset=["salary_min", "salary_max"]
    )

if not salary_df.empty:
    st.write(
        "The following listings contain numeric minimum "
        "and maximum salary values."
    )

    st.dataframe(
        salary_df[
            [
                "job_title",
                "company",
                "salary_min",
                "salary_max",
                "salary_currency",
                "salary_period",
            ]
        ],
        use_container_width=True
    )

    st.caption(
        "Compare salary figures only when the currency "
        "and pay period are the same."
    )
else:
    st.info(
        "No listings with both numeric minimum and maximum "
        "salary values are available for the selected jobs."
    )
