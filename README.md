# Remote Job Market Analyzer

## Project Overview

The **Remote Job Market Analyzer** is a Python-based data analytics project that explores remote job listings to identify in-demand skills, job roles, experience requirements, and available salary information.

The project uses data cleaning, exploratory data analysis (EDA), data visualization, and an interactive Streamlit dashboard to turn job listing data into actionable insights.

## Objectives

- Analyze the distribution of remote job roles.
- Identify the most frequently requested skills.
- Explore minimum experience requirements.
- Examine salary information where disclosed.
- Build an interactive dashboard to filter and explore job listings.

## Technology Stack

- **Python** — data analysis and processing
- **Pandas** — data manipulation
- **Matplotlib** — data visualization
- **Streamlit** — interactive dashboard
- **CSV** — dataset storage

## Key Features

- Dataset validation and data quality checks
- Job-title distribution analysis
- Skill frequency analysis
- Experience requirement analysis
- Salary analysis with missing-value handling
- Interactive job-title and experience filters
- Interactive job listing table

## Project Structure

```text
remote-job-market-analyzer/
├── data/
│   └── job_postings.csv
├── src/
│   ├── validate_data.py
│   ├── check_data_quality.py
│   ├── eda.py
│   └── dashboard.py
├── reports/
│   ├── top_10_skills.png
│   ├── skills_frequency.csv
│   ├── job_title_distribution.png
│   └── experience_requirements.png
├── .gitignore
├── requirements.txt
└── README.md
```

## Initial Findings

Based on the initial sample of 10 collected job listings:

- Data Analyst is the most frequent job title, appearing in 5 listings.
- SQL and Python each appear in 9 listings.
- Power BI and Statistics each appear in 6 listings.
- Seven listings contain minimum and maximum experience information.
- Salary information is incomplete, so salary analysis is limited to listings with numeric salary values.

**Note:** These findings describe the current sample only and should not be interpreted as representative of the entire remote job market. Listings have not necessarily been independently verified.

## How to Run the Project

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd remote-job-market-analyzer
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with the actual repository URL.

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run data analysis

```bash
python src/eda.py
```

### 4. Launch the dashboard

```bash
streamlit run src/dashboard.py
```

## Future Improvements

- Collect a larger and regularly updated dataset.
- Normalize skill names and categories.
- Add salary comparisons by currency and pay period.
- Include location and work-shift filters.
- Add automated data collection from permitted sources.
- Deploy the dashboard online.

## Disclaimer

This project is intended for educational and portfolio purposes. Results depend on the collected dataset, its completeness, and the accuracy of the recorded job information.
