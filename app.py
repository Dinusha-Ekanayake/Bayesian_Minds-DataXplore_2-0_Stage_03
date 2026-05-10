"""
DataXplore 2.0 — Overview Page
Company X Audience Analytics Dashboard
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st

from src.data_prep import prepare_data
from src.filters import render_sidebar_filters
from src.kpi import (
    TotalRevenue, RepeatVisitRate, AverageSatisfaction,
    fmt_currency, fmt_pct, fmt_score, fmt_count,
)
from src.styles import inject_css, render_kpi_row, section_header, page_header
from src.star_schema import build_star_schema

st.set_page_config(
    page_title="DataXplore 2.0 | Company X Analytics",
    page_icon="•",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

df_full = prepare_data()
df = render_sidebar_filters(df_full)

# ── Page Header ───────────────────────────────────────────────────────────────
page_header(
    "DataXplore 2.0",
    "Company X Live Entertainment — Customer Analytics Dashboard",
)

st.markdown("---")

# ── KPI Row ───────────────────────────────────────────────────────────────────
section_header("Key Performance Indicators")

total_rev = TotalRevenue(df)
total_customers = len(df)
repeat_rate = RepeatVisitRate(df)
avg_satisfaction = AverageSatisfaction(df)

render_kpi_row([
    {"label": "Total Revenue",       "value": fmt_currency(total_rev),    "category": "revenue"},
    {"label": "Total Customers",     "value": fmt_count(total_customers), "category": "customer"},
    {"label": "Repeat Visit Rate",   "value": fmt_pct(repeat_rate),       "category": "time"},
    {"label": "Avg Satisfaction",    "value": fmt_score(avg_satisfaction), "category": "experience"},
])

st.markdown("---")

# ── Project Description ───────────────────────────────────────────────────────
col1, col2 = st.columns([1.6, 1])

with col1:
    section_header("About This Dashboard")
    st.markdown("""
    This interactive business intelligence dashboard was built for the **DataXplore 2.0** hackathon,
    analyzing customer behaviour, revenue performance, and experience quality for **Company X**,
    a fictional live entertainment venue.

    **Dataset:** 800 customer records across 9 months (Jan – Sep 2025), covering 7 countries and 4 seating tiers.

    **Dashboard Sections:**
    | Page | Focus |
    |---|---|
    | **Revenue Analysis** | Ticket, merchandise & drink revenue by region, country, age |
    | **Customer Analysis** | Demographics, geographic distribution, spending behaviour |
    | **Experience Analysis** | Satisfaction scores, recommendation likelihood, correlations |
    | **Time-Based Analysis** | Monthly trends, seasonal patterns, day-of-week heatmap |

    Use the **sidebar filters** to slice data by date, country, seating region, gender, age group,
    and visit type. Filters persist across all pages.
    """)

with col2:
    section_header("Star Schema Model")
    st.image("model.jpeg", use_container_width=True)

st.markdown("---")

# ── Dataset Quick Stats ───────────────────────────────────────────────────────
section_header("Dataset Overview")

schema = build_star_schema()
fact = schema["fact_transactions"]
dim_c = schema["dim_customer"]
dim_d = schema["dim_date"]
dim_s = schema["dim_seating"]
dim_g = schema["dim_geography"]

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("fact_transactions", f"{len(fact):,} rows")
with col2:
    st.metric("dim_customer", f"{len(dim_c):,} rows")
with col3:
    st.metric("dim_date", f"{len(dim_d):,} rows")
with col4:
    st.metric("dim_seating", f"{len(dim_s):,} rows")
with col5:
    st.metric("dim_geography", f"{len(dim_g):,} rows")

st.markdown("---")

# ── Filtered Data Preview ─────────────────────────────────────────────────────
with st.expander("Filtered Data Preview — first 50 rows"):
    st.dataframe(
        df.head(50),
        use_container_width=True,
        height=300,
    )
