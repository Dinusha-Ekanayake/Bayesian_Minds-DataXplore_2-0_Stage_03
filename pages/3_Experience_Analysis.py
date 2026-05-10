"""
Experience Analysis Page
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st

from src.data_prep import prepare_data
from src.filters import render_sidebar_filters
from src.kpi import (
    AverageSatisfaction, AverageRecommendation, HighlySatisfiedPct,
    fmt_score, fmt_pct, fmt_count,
)
from src.styles import inject_css, render_kpi_row, section_header, page_header
from src.charts import (
    fig_satisfaction_by_region_visittype,
    fig_recommendation_by_country,
    fig_spend_vs_satisfaction,
    fig_spend_vs_recommendation,
    fig_correlation_heatmap,
    fig_satisfaction_violin,
    fig_radar_country_comparison,
)

st.set_page_config(
    page_title="Experience Analysis | DataXplore 2.0",
    page_icon="•",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

df_full = prepare_data()
df = render_sidebar_filters(df_full)

page_header("Experience Analysis", "Satisfaction scores, recommendation likelihood & correlations")
st.markdown("---")

# ── KPI Row ───────────────────────────────────────────────────────────────────
section_header("Experience KPIs")

avg_sat = AverageSatisfaction(df)
avg_rec = AverageRecommendation(df)
highly_sat = HighlySatisfiedPct(df, threshold=7.0)
highly_likely = (
    (df["Recommendation_Likelihood"] >= 7).sum() / len(df) * 100
    if len(df) > 0 else 0.0
)

render_kpi_row([
    {"label": "Avg Satisfaction",        "value": fmt_score(avg_sat),    "category": "experience"},
    {"label": "Avg Recommendation",      "value": fmt_score(avg_rec),    "category": "experience"},
    {"label": "Highly Satisfied (≥7)",   "value": fmt_pct(highly_sat),   "category": "experience"},
    {"label": "Likely to Recommend (≥7)","value": fmt_pct(highly_likely),"category": "experience"},
])

st.markdown("---")

# ── Row 1 ─────────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    section_header("Satisfaction by Region & Visit Type")
    if len(df) > 0:
        st.plotly_chart(fig_satisfaction_by_region_visittype(df), use_container_width=True)
    else:
        st.info("No data for current filters.")

with col2:
    section_header("Recommendation by Country & Visit Type")
    if len(df) > 0:
        st.plotly_chart(fig_recommendation_by_country(df), use_container_width=True)
    else:
        st.info("No data for current filters.")

st.markdown("---")

# ── Row 2: Scatter + Trendlines ───────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    section_header("Spend vs Satisfaction Score")
    if len(df) > 0:
        st.plotly_chart(fig_spend_vs_satisfaction(df), use_container_width=True)
    else:
        st.info("No data for current filters.")

with col2:
    section_header("Spend vs Recommendation Likelihood")
    if len(df) > 0:
        st.plotly_chart(fig_spend_vs_recommendation(df), use_container_width=True)
    else:
        st.info("No data for current filters.")

st.markdown("---")

# ── Row 3: Correlation & Violin ───────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    section_header("Correlation Matrix")
    if len(df) > 0:
        st.plotly_chart(fig_correlation_heatmap(df), use_container_width=True)
    else:
        st.info("No data for current filters.")

with col2:
    section_header("Satisfaction Distribution by Region")
    if len(df) > 0:
        st.plotly_chart(fig_satisfaction_violin(df), use_container_width=True)
    else:
        st.info("No data for current filters.")

st.markdown("---")

# ── Radar Chart ───────────────────────────────────────────────────────────────
section_header("Country Comparison Radar")
if len(df) > 0:
    st.plotly_chart(fig_radar_country_comparison(df), use_container_width=True)
else:
    st.info("No data for current filters.")
