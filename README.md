# Remote Job Market Analyzer

## Project Overview

The **Remote Job Market Analyzer** is a Python-based data analytics project designed to explore job listings, identify frequently requested skills, analyze experience requirements, and examine available salary information.

The project combines data validation, data cleaning, exploratory data analysis (EDA), data visualization, and an interactive Streamlit dashboard. It also includes a separate historical analysis of Data Analyst skills using a Kaggle job-postings dataset.

## Live Dashboard

**[Explore the Remote Job Market Analyzer](https://remote-job-market-analyzer-czwwnzxwdzmci4zcttt3bp.streamlit.app/)**

The interactive dashboard allows users to:
- Explore job listings by job title and location.
- Filter listings by minimum experience requirements.
- Analyze frequently requested skills.
- Review available salary information.
- Explore historical Data Analyst skill trends.

## Project Objectives

- Analyze job titles and listing characteristics.
- Identify frequently mentioned Data Analyst skills.
- Explore experience requirements.
- Examine salary information where available.
- Build an interactive dashboard for exploring job listings.
- Apply data quality checks and data visualization techniques to real-world datasets.

## Technology Stack

- **Python** — data processing and analysis
- **Pandas** — data cleaning and manipulation
- **Matplotlib** — data visualization
- **Streamlit** — interactive dashboard
- **CSV** — data storage and analytical reports
- **Git and GitHub** — version control and project hosting

## Key Features

- Dataset validation and data quality checks.
- Exploratory data analysis and job-title distribution.
- Skill frequency analysis and standardized skill labels.
- Experience requirement analysis.
- Salary analysis with missing-value handling.
- Interactive job-title and location filters.
- Experience-range filtering.
- Historical Data Analyst skills table and top-10 skills chart.
- Interactive job listing table.

## Project Structure

```text
remote-job-market-analyzer/
├── data/
│   ├── job_postings.csv
│   └── kaggle_data/
│       ├── job_postings.csv
│       ├── job_skills.csv
│       └── job_summaries.csv
├── src/
│   ├── validate_data.py
│   ├── check_data_quality.py
│   ├── eda.py
│   ├── dashboard.py
│   └── inspect_kaggle_data.py
├── reports/
│   ├── top_10_skills.png
│   ├── skills_frequency.csv
│   ├── job_title_distribution.png
│   ├── experience_requirements.png
│   ├── data_analyst_skill_frequency.csv
│   ├── data_analyst_skill_frequency_cleaned.csv
│   ├── top_10_data_analyst_skills.png
│   └── dashboard_screenshot.png
├── .gitignore
├── requirements.txt
└── README.md
```

## Data Sources

### 1. Initial Job Listings

The initial dataset, `data/job_postings.csv`, contains 10 manually collected job listings used to develop and test the dashboard.

These records support the initial job listing, skill, experience, and salary analysis.

### 2. Kaggle Job Postings and Skills Dataset

The project also uses the **Data Science Job Postings and Skills** dataset from Kaggle.

**Source:** https://www.kaggle.com/datasets/asaniczka/data-science-job-postings-and-skills

The downloaded files include:
- `job_postings.csv`
- `job_skills.csv`
- `job_summaries.csv`

The dataset contains 12,217 job postings and covers records first seen between January 12 and January 17, 2024.

The Kaggle data is analyzed separately to examine skill mentions in job postings with Data Analyst in the title. Its skills report is displayed in the dashboard's historical insights section.

## Key Findings

### Initial Job Listings

Based on the initial sample of 10 job listings:

- Data Analyst is the most frequent job title, appearing in 5 listings.
- SQL and Python each appear in 9 listings.
- Power BI and Statistics each appear in 6 listings.
- Seven listings contain minimum and maximum experience information.
- Salary analysis is limited because salary information is incomplete.

### Historical Data Analyst Skills Analysis

The cleaned Kaggle skills report identified the following top 10 skill mentions:

| Skill | Mentions |
|---|---:|
| Data Analysis | 1,709 |
| SQL | 1,179 |
| Data Visualization | 1,008 |
| Communication | 870 |
| Python | 824 |
| Tableau | 744 |
| Power BI | 583 |
| R | 569 |
| Excel | 523 |
| Data Mining | 383 |

These values represent skill mentions counted from the dataset's comma-separated skill labels. They should not be interpreted as verified counts of unique job postings requiring each skill.

## How to Run the Project Locally

### 1. Clone the repository

Replace `YOUR_GITHUB_REPOSITORY_URL` with the actual URL of your GitHub repository.

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd remote-job-market-analyzer
```

### 2. Create and activate a virtual environment

On Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run data analysis

```bash
python src/eda.py
```

### 5. Inspect the Kaggle dataset

Ensure the three Kaggle CSV files are present in `data/kaggle_data/`, then run:

```bash
python src/inspect_kaggle_data.py
```

This script generates the historical Data Analyst skills reports and visualization.

### 6. Launch the dashboard

```bash
python -m streamlit run src/dashboard.py
```

Streamlit will provide a local URL where the dashboard can be accessed.

## Data Limitations

- The initial dataset contains only 10 manually collected listings and is not representative of the entire job market.
- The Kaggle dataset covers a short historical period in January 2024 and should not be treated as a source of current job-market demand.
- The Kaggle dataset contains relatively few listings labeled as remote.
- Missing salary values and differences in currencies and pay periods limit direct salary comparisons.
- Skill counts represent mentions in the dataset's skill labels, not necessarily the number of unique job postings requiring each skill.
- The results depend on the completeness, accuracy, and labeling of the underlying datasets.

## Future Improvements

- Collect a larger, regularly updated dataset from permitted sources.
- Improve skill-name standardization and skill categorization.
- Add salary comparisons by currency, pay period, role, and experience level.
- Expand location and work-shift filters.
- Improve data validation and automated reporting.
- Explore predictive modeling for salary estimation when sufficient suitable data is available.
- Add automated tests and further improve dashboard usability.

## Disclaimer

This project is intended for educational and portfolio purposes. The findings are exploratory and depend on the quality, completeness, and time period of the datasets used. Historical skill mentions should not be interpreted as current hiring trends or guarantees of employment.
