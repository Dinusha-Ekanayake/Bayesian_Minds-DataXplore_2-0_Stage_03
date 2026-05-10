# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

The app runs at http://localhost:8501. No build step or test suite exists.

## Architecture

This is a 5-page Streamlit analytics dashboard for Company X customer data.

**Data pipeline (all cached with `@st.cache_data`):**
```
data/Company_X_Audience.csv
  → src/data_loader.py   (load CSV)
  → src/data_prep.py     (type casting + 8 derived columns)
  → src/star_schema.py   (split into fact + 4 dimension tables)
  → src/filters.py       (sidebar filter logic, persisted via st.session_state)
  → src/kpi.py           (aggregate metrics + formatters)
  → src/charts.py        (25+ Plotly figure factory functions)
  → src/styles.py        (CSS injection, KPI card HTML, color palettes)
```

**Pages:**
- `app.py` — Overview: KPIs and star schema visualization
- `pages/1_Revenue_Analysis.py` — Revenue by region/country/age
- `pages/2_Customer_Analysis.py` — Demographics and spending patterns
- `pages/3_Experience_Analysis.py` — Satisfaction and recommendation analysis
- `pages/4_Time_Based_Analysis.py` — Monthly trends and temporal patterns

**Key design patterns:**
- All chart functions live in `src/charts.py` and return Plotly figures — add new visualizations there
- Color palettes (by seating tier, gender, country, age group, revenue stream) are centralized in `src/styles.py`
- Filters are applied at the page level after loading from `src/filters.py`; the filtered DataFrame is passed into KPI and chart functions
- `src/star_schema.py` builds normalized dimension tables from the flat CSV — use these for BI-style joins if needed

**Dataset:** 800 customer records, 9 months (Jan–Sep 2025), 7 countries, 4 seating tiers (VIP $200, Premium $150, High Economy $100, Economy $60). No nulls, no duplicate Customer_IDs. Derived columns added in prep: `Ticket_Revenue`, `Total_Spend`, `Month_Label`, `Age_Group`, `Visit_Type`, `Spend_Tier`.

**Theme:** Dark (configured in `.streamlit/config.toml`). Primary accent: `#FF6B6B`. Background: `#0E1117`.
