import pandas as pd
import streamlit as st

from src.data_prep import prepare_data
from src.styles import inject_css


def _setup_multi_pill(df: pd.DataFrame, col_name: str, logical_key: str, ui_key: str) -> list:
    """Safely initializes and restores widget state across page navigations."""
    all_options = sorted(df[col_name].unique().tolist())
    
    # Custom sort for Age Group logically
    if col_name == "Age_Group":
        all_options = sorted(all_options, key=lambda x: int(x.split("-")[0].replace("+", "").strip()))

    # 1. First-time initialization
    if logical_key not in st.session_state:
        st.session_state[logical_key] = all_options
        st.session_state[ui_key] = ["All"]
        st.session_state[f"{ui_key}_prev"] = ["All"]
        
    # 2. RESTORE UI STATE if Streamlit deleted it during a page swap
    if ui_key not in st.session_state:
        if len(st.session_state[logical_key]) == len(all_options):
            st.session_state[ui_key] = ["All"]
        else:
            st.session_state[ui_key] = st.session_state[logical_key].copy()
        st.session_state[f"{ui_key}_prev"] = st.session_state[ui_key].copy()
        
    return all_options


def _pill_callback(ui_key: str, logical_key: str, all_options: list):
    """Handles the 'All' mutual exclusivity and syncs UI to Logic."""
    current = st.session_state[ui_key]
    prev = st.session_state.get(f"{ui_key}_prev", ["All"])
    
    if "All" in current and "All" not in prev:
        # User clicked "All" -> clear everything else
        current = ["All"]
    elif "All" in current and len(current) > 1:
        # User clicked an option while "All" was active -> remove "All"
        current.remove("All")
    elif not current:
        # User deselected everything -> fallback to "All"
        current = ["All"]
        
    # Update UI state
    st.session_state[ui_key] = current
    st.session_state[f"{ui_key}_prev"] = current.copy()
    
    # Update Logical state
    if "All" in current:
        st.session_state[logical_key] = all_options
    else:
        st.session_state[logical_key] = current


def _visit_type_callback():
    """Ensures Visit Type never stays empty."""
    if not st.session_state["_ui_visit_type"]:
        st.session_state["_ui_visit_type"] = "All"
    st.session_state["filter_visit_type"] = st.session_state["_ui_visit_type"]


def render_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Render sidebar filters and return the filtered DataFrame."""
    
    # ── Initialize & Restore States ───────────────────────────────────────
    if "filter_date_range" not in st.session_state:
        min_date = df["Visit_Date"].min().date()
        max_date = df["Visit_Date"].max().date()
        st.session_state["filter_date_range"] = (min_date, max_date)

    all_countries = _setup_multi_pill(df, "Country", "filter_countries", "_ui_countries")
    all_seating = _setup_multi_pill(df, "Seating_Region", "filter_seating", "_ui_seating")
    all_genders = _setup_multi_pill(df, "Gender", "filter_gender", "_ui_gender")
    all_age_groups = _setup_multi_pill(df, "Age_Group", "filter_age_groups", "_ui_age")

    if "filter_visit_type" not in st.session_state:
        st.session_state["filter_visit_type"] = "All"
    if "_ui_visit_type" not in st.session_state:
        st.session_state["_ui_visit_type"] = st.session_state["filter_visit_type"]

    with st.sidebar:
        st.markdown("## Filters")
        st.markdown("---")

        # ── Date Range ────────────────────────────────────────────────────
        st.markdown("**Date Range**")
        min_date_val = df["Visit_Date"].min().date()
        max_date_val = df["Visit_Date"].max().date()
        
        date_range = st.date_input(
            "Select date range",
            value=st.session_state["filter_date_range"],
            min_value=min_date_val,
            max_value=max_date_val,
            label_visibility="collapsed",
        )
        if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
            st.session_state["filter_date_range"] = (date_range[0], date_range[1])
        elif isinstance(date_range, (list, tuple)) and len(date_range) == 1:
            st.session_state["filter_date_range"] = (date_range[0], max_date_val)

        st.markdown("---")

        # ── Countries ─────────────────────────────────────────────────────
        st.markdown("**Countries**")
        st.pills(
            "Countries",
            options=["All"] + all_countries,
            selection_mode="multi",
            key="_ui_countries",
            on_change=_pill_callback,
            args=("_ui_countries", "filter_countries", all_countries),
            label_visibility="collapsed"
        )

        # ── Seating Region ────────────────────────────────────────────────
        st.markdown("**Seating Region**")
        st.pills(
            "Seating Region",
            options=["All"] + all_seating,
            selection_mode="multi",
            key="_ui_seating",
            on_change=_pill_callback,
            args=("_ui_seating", "filter_seating", all_seating),
            label_visibility="collapsed"
        )

        # ── Gender ────────────────────────────────────────────────────────
        st.markdown("**Gender**")
        st.pills(
            "Gender",
            options=["All"] + all_genders,
            selection_mode="multi",
            key="_ui_gender",
            on_change=_pill_callback,
            args=("_ui_gender", "filter_gender", all_genders),
            label_visibility="collapsed"
        )

        # ── Age Group ─────────────────────────────────────────────────────
        st.markdown("**Age Group**")
        st.pills(
            "Age Group",
            options=["All"] + all_age_groups,
            selection_mode="multi",
            key="_ui_age",
            on_change=_pill_callback,
            args=("_ui_age", "filter_age_groups", all_age_groups),
            label_visibility="collapsed"
        )

        # ── Visit Type ────────────────────────────────────────────────────
        st.markdown("**Visit Type**")
        st.pills(
            "Visit Type",
            options=["All", "First-time", "Repeat"],
            selection_mode="single",
            key="_ui_visit_type",
            on_change=_visit_type_callback,
            label_visibility="collapsed"
        )

        st.markdown("---")

        # ── Reset Button ──────────────────────────────────────────────────
        if st.button("Reset Filters", use_container_width=True):
            keys_to_clear = [k for k in st.session_state.keys() if k.startswith("filter_") or k.startswith("_ui_")]
            for k in keys_to_clear:
                del st.session_state[k]
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