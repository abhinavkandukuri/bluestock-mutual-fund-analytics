# SQL Analysis — Mutual Fund Analytics

## Database

Database: `mutual_fund.db`

The project uses SQLite for structured analysis of mutual fund,
NAV, investor transaction, AUM, category inflow, and portfolio data.

## Tables

1. `fund_analysis`
2. `nav_analysis`
3. `transactions`
4. `category_inflows`
5. `aum_analysis`
6. `portfolio_holdings`

---

## SQL Analysis Performed

### Fund Performance

- Top funds by 1-year return
- Fund houses by average 3-year return
- Category-level performance
- Top funds by Alpha
- Top funds by Sharpe Ratio
- Funds performing above the average 3-year return
- Best-performing fund in each category
- Funds with both above-average return and Sharpe Ratio

### Fund House Analysis

- Fund houses with the highest number of funds
- Fund house AUM comparison

### Investor & Transaction Analysis

- Transaction type analysis
- T30 vs B30 transaction comparison
- Monthly transaction trends
- KYC status analysis

### Portfolio Analysis

- Top stock holdings
- Most diversified funds
- Sector concentration

---

## Important SQL Concepts Used

The analysis demonstrates:

- SELECT
- WHERE
- GROUP BY
- ORDER BY
- LIMIT
- COUNT()
- SUM()
- AVG()
- MAX()
- DISTINCT
- Subqueries
- Correlated subqueries
- Aggregate filtering

---

## Key Business Questions Answered

The SQL analysis helps answer:

1. Which mutual funds have the strongest historical returns?
2. Which fund houses show stronger average performance?
3. Which categories perform better?
4. Which funds generate higher Alpha?
5. Which funds provide better risk-adjusted returns?
6. Which categories attract the highest net inflows?
7. Which fund houses manage the largest AUM?
8. What type of transactions dominate investor activity?
9. How do T30 and B30 investors differ?
10. Which sectors have the highest portfolio concentration?
11. Which funds have more diversified portfolios?
12. Which funds combine strong returns with strong risk-adjusted performance?

---

## SQL File

The SQL analysis is implemented in:

`sql_analysis.py`

The SQLite database is stored in:

`sql/mutual_fund.db`
