"""
Customer Analysis Page
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st

from src.data_prep import prepare_data
from src.filters import render_sidebar_filters
from src.kpi import (
    RepeatVisitRate, AverageSpendPerCustomer,
    fmt_count, fmt_pct, fmt_currency, fmt_score,
)
from src.styles import inject_css, render_kpi_row, section_header, page_header
from src.charts import (
    fig_gender_donut,
    fig_seating_donut,
    fig_age_histogram,
    fig_choropleth,
    fig_spend_boxplot,
    fig_repeat_vs_firsttime_spend,
    fig_age_vs_spend_scatter,
)

st.set_page_config(
    page_title="Customer Analysis | DataXplore 2.0",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

df_full = prepare_data()
df = render_sidebar_filters(df_full)

page_header("👥 Customer Analysis", "Demographics, geographic distribution & spending behaviour")
st.markdown("---")

# ── KPI Row ───────────────────────────────────────────────────────────────────
section_header("Customer KPIs")

total_customers = len(df)
avg_tickets = df["Num_Tickets"].mean() if len(df) > 0 else 0
repeat_rate = RepeatVisitRate(df)
avg_spend = AverageSpendPerCustomer(df)

render_kpi_row([
    {"label": "Total Customers",    "value": fmt_count(total_customers),   "category": "customer"},
    {"label": "Avg Tickets / Visit","value": f"{avg_tickets:.2f}",         "category": "customer"},
    {"label": "Repeat Visit Rate",  "value": fmt_pct(repeat_rate),         "category": "time"},
    {"label": "Avg Spend",          "value": fmt_currency(avg_spend),      "category": "revenue"},
])

st.markdown("---")

# ── Row 1: Distribution Donuts ─────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    section_header("Gender Distribution")
    if len(df) > 0:
        st.plotly_chart(fig_gender_donut(df), use_container_width=True)
    else:
        st.info("No data for current filters.")

with col2:
    section_header("Seating Region Distribution")
    if len(df) > 0:
        st.plotly_chart(fig_seating_donut(df), use_container_width=True)
    else:
        st.info("No data for current filters.")

st.markdown("---")

# ── Row 2: Age & Geography ────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    section_header("Age Distribution by Gender")
    if len(df) > 0:
        st.plotly_chart(fig_age_histogram(df), use_container_width=True)
    else:
        st.info("No data for current filters.")

with col2:
    section_header("Geographic Distribution")
    if len(df) > 0:
        st.plotly_chart(fig_choropleth(df), use_container_width=True)
    else:
        st.info("No data for current filters.")

st.markdown("---")

# ── Row 3: Spending Analysis ──────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    section_header("Spend Distribution by Region")
    if len(df) > 0:
        st.plotly_chart(fig_spend_boxplot(df), use_container_width=True)
    else:
        st.info("No data for current filters.")

with col2:
    section_header("Repeat vs First-time Avg Spend")
    if len(df) > 0:
        st.plotly_chart(fig_repeat_vs_firsttime_spend(df), use_container_width=True)
    else:
        st.info("No data for current filters.")

st.markdown("---")

# ── Row 4: Scatter ────────────────────────────────────────────────────────────
section_header("Age vs Total Spend")
if len(df) > 0:
    st.plotly_chart(fig_age_vs_spend_scatter(df), use_container_width=True)
else:
    st.info("No data for current filters.")
