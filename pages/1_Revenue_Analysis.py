"""
Revenue Analysis Page
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st

from src.data_prep import prepare_data
from src.filters import render_sidebar_filters
from src.kpi import (
    TotalTicketRevenue, TotalMerchandiseRevenue, TotalDrinkRevenue,
    TotalRevenue, AverageSpendPerCustomer,
    fmt_currency,
)
from src.styles import inject_css, render_kpi_row, section_header, page_header
from src.charts import (
    fig_revenue_by_seating,
    fig_revenue_by_country,
    fig_seating_share_by_country,
    fig_revenue_by_age_group,
    fig_revenue_country_by_seating,
    fig_revenue_seating_by_gender,
)

st.set_page_config(
    page_title="Revenue Analysis | DataXplore 2.0",
    page_icon="•",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

df_full = prepare_data()
df = render_sidebar_filters(df_full)

page_header("Revenue Analysis", "Ticket, merchandise & drink revenue across segments")
st.markdown("---")

# ── KPI Row ───────────────────────────────────────────────────────────────────
section_header("Revenue KPIs")

render_kpi_row([
    {"label": "Total Revenue",          "value": fmt_currency(TotalRevenue(df)),              "category": "revenue"},
    {"label": "Ticket Revenue",         "value": fmt_currency(TotalTicketRevenue(df)),         "category": "revenue"},
    {"label": "Merchandise Revenue",    "value": fmt_currency(TotalMerchandiseRevenue(df)),    "category": "revenue"},
    {"label": "Drink Revenue",          "value": fmt_currency(TotalDrinkRevenue(df)),          "category": "revenue"},
])

st.markdown("---")

# ── Charts Row 1 ──────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    section_header("Revenue by Seating Region")
    if len(df) > 0:
        st.plotly_chart(fig_revenue_by_seating(df), use_container_width=True)
    else:
        st.info("No data for current filters.")

with col2:
    section_header("Revenue by Country")
    if len(df) > 0:
        st.plotly_chart(fig_revenue_by_country(df), use_container_width=True)
    else:
        st.info("No data for current filters.")

st.markdown("---")

# ── Charts Row 2 ──────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    section_header("Seating Region Share by Country")
    if len(df) > 0:
        st.plotly_chart(fig_seating_share_by_country(df), use_container_width=True)
    else:
        st.info("No data for current filters.")

with col2:
    section_header("Revenue by Age Group")
    if len(df) > 0:
        st.plotly_chart(fig_revenue_by_age_group(df), use_container_width=True)
    else:
        st.info("No data for current filters.")

st.markdown("---")

# ── Revenue Breakdown ─────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    section_header("Revenue by Country & Seating Tier")
    if len(df) > 0:
        st.plotly_chart(fig_revenue_country_by_seating(df), use_container_width=True)
    else:
        st.info("No data for current filters.")

with col2:
    section_header("Revenue by Seating Tier & Gender")
    if len(df) > 0:
        st.plotly_chart(fig_revenue_seating_by_gender(df), use_container_width=True)
    else:
        st.info("No data for current filters.")

st.markdown("---")

# ── Avg Spend KPI ──────────────────────────────────────────────────────────────
avg_spend = AverageSpendPerCustomer(df)
st.markdown(
    f"""<div style="background:linear-gradient(135deg,rgba(255,255,255,0.055) 0%,rgba(255,255,255,0.020) 100%);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-radius:16px;padding:18px 24px;border:1px solid rgba(255,255,255,0.07);border-left:4px solid #00C48C;display:inline-block;margin-top:8px;box-shadow:0 8px 32px rgba(0,0,0,0.45);">
    <span style="color:rgba(156,163,175,0.9);font-size:11px;text-transform:uppercase;letter-spacing:0.07em;font-weight:500;">Avg Spend per Customer</span>
    <br><span style="color:#FAFAFA;font-size:28px;font-weight:700;letter-spacing:-0.02em;">{fmt_currency(avg_spend)}</span>
    </div>""",
    unsafe_allow_html=True,
)
