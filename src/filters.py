import pandas as pd
import streamlit as st

from src.data_prep import prepare_data
from src.styles import inject_css


def _init_filters(df: pd.DataFrame):
    """Initialize session_state filter defaults if not set."""
    if "filter_initialized" not in st.session_state:
        min_date = df["Visit_Date"].min().date()
        max_date = df["Visit_Date"].max().date()

        st.session_state["filter_date_range"] = (min_date, max_date)
        st.session_state["filter_countries"] = sorted(df["Country"].unique().tolist())
        st.session_state["filter_seating"] = sorted(df["Seating_Region"].unique().tolist())
        st.session_state["filter_gender"] = sorted(df["Gender"].unique().tolist())
        st.session_state["filter_age_groups"] = sorted(
            df["Age_Group"].unique().tolist(),
            key=lambda x: int(x.split("-")[0].replace("+", "").strip()),
        )
        st.session_state["filter_visit_type"] = "All"
        st.session_state["filter_initialized"] = True


def render_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Render sidebar filters and return the filtered DataFrame."""
    _init_filters(df)

    with st.sidebar:
        st.markdown("## Filters")
        st.markdown("---")

        # ── Date Range ────────────────────────────────────────────────────
        min_date = df["Visit_Date"].min().date()
        max_date = df["Visit_Date"].max().date()

        st.markdown("**Date Range**")
        date_range = st.date_input(
            "Select date range",
            value=st.session_state["filter_date_range"],
            min_value=min_date,
            max_value=max_date,
            key="_date_range_widget",
            label_visibility="collapsed",
        )
        if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
            st.session_state["filter_date_range"] = (date_range[0], date_range[1])
        elif isinstance(date_range, (list, tuple)) and len(date_range) == 1:
            st.session_state["filter_date_range"] = (date_range[0], max_date)

        st.markdown("---")

        # ── Country ───────────────────────────────────────────────────────
        all_countries = sorted(df["Country"].unique().tolist())
        selected_countries = st.multiselect(
            "Countries",
            options=all_countries,
            default=st.session_state["filter_countries"],
            key="_countries_widget",
        )
        st.session_state["filter_countries"] = selected_countries if selected_countries else all_countries

        # ── Seating Region ────────────────────────────────────────────────
        all_seating = sorted(df["Seating_Region"].unique().tolist())
        selected_seating = st.multiselect(
            "Seating Region",
            options=all_seating,
            default=st.session_state["filter_seating"],
            key="_seating_widget",
        )
        st.session_state["filter_seating"] = selected_seating if selected_seating else all_seating

        # ── Gender ────────────────────────────────────────────────────────
        all_genders = sorted(df["Gender"].unique().tolist())
        selected_genders = st.multiselect(
            "Gender",
            options=all_genders,
            default=st.session_state["filter_gender"],
            key="_gender_widget",
        )
        st.session_state["filter_gender"] = selected_genders if selected_genders else all_genders

        # ── Age Group ─────────────────────────────────────────────────────
        all_age_groups = sorted(
            df["Age_Group"].unique().tolist(),
            key=lambda x: int(x.split("-")[0].replace("+", "").strip()),
        )
        selected_age_groups = st.multiselect(
            "Age Group",
            options=all_age_groups,
            default=st.session_state["filter_age_groups"],
            key="_age_groups_widget",
        )
        st.session_state["filter_age_groups"] = selected_age_groups if selected_age_groups else all_age_groups

        # ── Visit Type ────────────────────────────────────────────────────
        visit_type = st.radio(
            "Visit Type",
            options=["All", "First-time", "Repeat"],
            index=["All", "First-time", "Repeat"].index(st.session_state["filter_visit_type"]),
            key="_visit_type_widget",
            horizontal=True,
        )
        st.session_state["filter_visit_type"] = visit_type

        st.markdown("---")

        # Reset button
        if st.button("Reset Filters", use_container_width=True):
            for key in list(st.session_state.keys()):
                if key.startswith("filter_"):
                    del st.session_state[key]
            st.rerun()

        # ── Stats ─────────────────────────────────────────────────────────
        st.markdown("### Dataset")
        st.caption(f"Total records: **{len(df):,}**")

    # ── Apply Filters ─────────────────────────────────────────────────────
    date_start, date_end = st.session_state["filter_date_range"]
    mask = (
        (df["Visit_Date"].dt.date >= date_start)
        & (df["Visit_Date"].dt.date <= date_end)
        & (df["Country"].isin(st.session_state["filter_countries"]))
        & (df["Seating_Region"].isin(st.session_state["filter_seating"]))
        & (df["Gender"].isin(st.session_state["filter_gender"]))
        & (df["Age_Group"].isin(st.session_state["filter_age_groups"]))
    )
    if st.session_state["filter_visit_type"] != "All":
        mask &= df["Visit_Type"] == st.session_state["filter_visit_type"]

    filtered = df[mask].copy()

    # Show filtered count in sidebar
    with st.sidebar:
        st.caption(f"Filtered records: **{len(filtered):,}**")

    return filtered
