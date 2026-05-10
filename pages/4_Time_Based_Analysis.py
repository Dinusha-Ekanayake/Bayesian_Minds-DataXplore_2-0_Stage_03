"""
Time-Based Analysis Page
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import pandas as pd

from src.data_prep import prepare_data
from src.filters import render_sidebar_filters
from src.styles import inject_css, render_kpi_row, section_header, page_header
from src.charts import (
    fig_monthly_revenue_trend,
    fig_monthly_revenue_streams,
    fig_monthly_satisfaction,
    fig_visit_heatmap,
    fig_monthly_repeat_rate,
    fig_monthly_customers_by_region,
    _monthly_df,
)

st.set_page_config(
    page_title="Time-Based Analysis | DataXplore 2.0",
    page_icon="•",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

df_full = prepare_data()
df = render_sidebar_filters(df_full)

page_header("Time-Based Analysis", "Monthly revenue trends, seasonal patterns & temporal insights")
st.markdown("---")

# ── KPI Row ───────────────────────────────────────────────────────────────────
section_header("Time-Based KPIs")

if len(df) > 0:
    mdf = _monthly_df(df)

    best_month_row = mdf.loc[mdf["Total_Revenue"].idxmax()]
    worst_month_row = mdf.loc[mdf["Total_Revenue"].idxmin()]
    best_month = best_month_row["Month_Label"]
    worst_month = worst_month_row["Month_Label"]

    # Month-over-Month growth (last two months)
    if len(mdf) >= 2:
        last = mdf.iloc[-1]["Total_Revenue"]
        prev = mdf.iloc[-2]["Total_Revenue"]
        mom_growth = (last - prev) / prev * 100 if prev > 0 else 0.0
        mom_label = f"{'+' if mom_growth >= 0 else ''}{mom_growth:.1f}%"
    else:
        mom_label = "N/A"

    # Peak day of week
    df2 = df.copy()
    df2["Day_of_Week"] = df2["Visit_Date"].dt.day_name()
    peak_day = df2["Day_of_Week"].value_counts().idxmax()

    render_kpi_row([
        {"label": "Best Revenue Month",  "value": best_month,  "category": "revenue"},
        {"label": "Worst Revenue Month", "value": worst_month, "category": "customer"},
        {"label": "MoM Revenue Growth",  "value": mom_label,   "category": "time"},
        {"label": "Peak Day of Week",    "value": peak_day,    "category": "experience"},
    ])
else:
    st.info("No data for current filters.")

st.markdown("---")

# ── Monthly Revenue Trend ─────────────────────────────────────────────────────
section_header("Monthly Revenue Trend")
if len(df) > 0:
    st.plotly_chart(fig_monthly_revenue_trend(df), use_container_width=True)
else:
    st.info("No data for current filters.")

st.markdown("---")

# ── Revenue Streams ───────────────────────────────────────────────────────────
section_header("Monthly Revenue by Stream (Stacked Area)")
if len(df) > 0:
    st.plotly_chart(fig_monthly_revenue_streams(df), use_container_width=True)
else:
    st.info("No data for current filters.")

st.markdown("---")

# ── Row: Satisfaction & Heatmap ───────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    section_header("Monthly Avg Satisfaction Trend")
    if len(df) > 0:
        st.plotly_chart(fig_monthly_satisfaction(df), use_container_width=True)
    else:
        st.info("No data for current filters.")

with col2:
    section_header("Visit Heatmap: Day of Week × Month")
    if len(df) > 0:
        st.plotly_chart(fig_visit_heatmap(df), use_container_width=True)
    else:
        st.info("No data for current filters.")

st.markdown("---")

# ── Row: Repeat Rate & Customers by Region ────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    section_header("Monthly Repeat Visit Rate")
    if len(df) > 0:
        st.plotly_chart(fig_monthly_repeat_rate(df), use_container_width=True)
    else:
        st.info("No data for current filters.")

with col2:
    section_header("Monthly Customers by Seating Region")
    if len(df) > 0:
        st.plotly_chart(fig_monthly_customers_by_region(df), use_container_width=True)
    else:
        st.info("No data for current filters.")
