# Bluestock Mutual Fund Analytics Platform

An end-to-end Mutual Fund Analytics Platform developed as part of the **Bluestock Fintech Data Analyst Internship Capstone Project**.

The project covers the complete data analytics workflow — from data ingestion and cleaning to SQL database design, exploratory data analysis, performance and risk analytics, investor analytics, and interactive Power BI dashboards.

---

## 📌 Project Overview

Mutual fund investors need reliable insights into fund performance, risk, investor behavior, market trends, and benchmark comparisons.

This project builds an analytics platform that processes mutual fund datasets and transforms raw financial data into meaningful business insights through:

- Python-based data ingestion and ETL
- Data cleaning and validation
- SQLite database and star schema
- SQL analytical queries
- Exploratory Data Analysis (EDA)
- Mutual fund performance analytics
- Risk analysis
- Investor transaction analysis
- SIP and market trend analysis
- Power BI interactive dashboards
- Advanced analytics and recommendation logic

---

## 🎯 Project Objectives

The main objectives of this project are:

1. Collect and ingest mutual fund data.
2. Clean, validate, and transform the datasets.
3. Design a structured SQL database using a star schema.
4. Perform exploratory data analysis.
5. Calculate mutual fund performance and risk metrics.
6. Analyze investor transactions and SIP behavior.
7. Compare fund performance against benchmark indices.
8. Build interactive dashboards using Power BI.
9. Generate investor-focused insights and recommendations.
10. Document the complete analytics workflow.

---

## 🗂️ Project Structure

```text
bluestock-mf-capstone/
│
├── data/
│   ├── raw/
│   │   ├── 01_fund_master.csv
│   │   ├── 02_nav_history.csv
│   │   ├── 03_aum_by_fund_house.csv
│   │   ├── 04_monthly_sip_inflows.csv
│   │   ├── 05_category_inflows.csv
│   │   ├── 06_industry_folio_count.csv
│   │   ├── 07_scheme_performance.csv
│   │   ├── 08_investor_transactions.csv
│   │   ├── 09_portfolio_holdings.csv
│   │   └── 10_benchmark_indices.csv
│   │
│   └── processed/
│       ├── 01_fund_master_clean.csv
│       ├── 02_nav_history_clean.csv
│       ├── 03_aum_by_fund_house_clean.csv
│       ├── 04_monthly_sip_inflows_clean.csv
│       ├── 05_category_inflows_clean.csv
│       ├── 06_industry_folio_count_clean.csv
│       ├── 07_scheme_performance_clean.csv
│       ├── 08_investor_transactions_clean.csv
│       ├── 09_portfolio_holdings_clean.csv
│       └── 10_benchmark_indices_clean.csv
│
├── db/
│   └── bluestock_mf.db
│
├── notebooks/
│   ├── 01_data_ingestion.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda_analysis.ipynb
│   ├── 04_performance_analytics.ipynb
│   └── 05_advanced_analytics.ipynb
│
├── scripts/
│   ├── data_ingestion.py
│   ├── live_nav_fetch.py
│   ├── etl_pipeline.py
│   ├── compute_metrics.py
│   └── recommender.py
│
├── sql/
│   ├── schema.sql
│   └── queries.sql
│
├── dashboard/
│   └── bluestock_mf_dashboard.pbix
│
├── reports/
│   ├── Final_Report.pdf
│   └── Presentation.pptx
│
├── data_dictionary.md
├── data_quality_report.csv
├── database_row_counts.csv
├── requirements.txt
├── .gitignore
└── README.md
