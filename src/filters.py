# # import pandas as pd
# # import streamlit as st

# # from src.data_prep import prepare_data
# # from src.styles import inject_css


# # def _init_filters(df: pd.DataFrame):
# #     """Initialize session_state filter defaults if not set."""
# #     if "filter_initialized" not in st.session_state:
# #         min_date = df["Visit_Date"].min().date()
# #         max_date = df["Visit_Date"].max().date()

# #         st.session_state["filter_date_range"] = (min_date, max_date)
# #         st.session_state["filter_countries"] = sorted(df["Country"].unique().tolist())
# #         st.session_state["filter_seating"] = sorted(df["Seating_Region"].unique().tolist())
# #         st.session_state["filter_gender"] = sorted(df["Gender"].unique().tolist())
# #         st.session_state["filter_age_groups"] = sorted(
# #             df["Age_Group"].unique().tolist(),
# #             key=lambda x: int(x.split("-")[0].replace("+", "").strip()),
# #         )
# #         st.session_state["filter_visit_type"] = "All"
# #         st.session_state["filter_initialized"] = True


# # def render_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
# #     """Render sidebar filters and return the filtered DataFrame."""
# #     _init_filters(df)

# #     with st.sidebar:
# #         st.markdown("## Filters")
# #         st.markdown("---")

# #         # ── Date Range ────────────────────────────────────────────────────
# #         min_date = df["Visit_Date"].min().date()
# #         max_date = df["Visit_Date"].max().date()

# #         st.markdown("**Date Range**")
# #         date_range = st.date_input(
# #             "Select date range",
# #             value=st.session_state["filter_date_range"],
# #             min_value=min_date,
# #             max_value=max_date,
# #             key="_date_range_widget",
# #             label_visibility="collapsed",
# #         )
# #         if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
# #             st.session_state["filter_date_range"] = (date_range[0], date_range[1])
# #         elif isinstance(date_range, (list, tuple)) and len(date_range) == 1:
# #             st.session_state["filter_date_range"] = (date_range[0], max_date)

# #         st.markdown("---")

# #         # ── Country ───────────────────────────────────────────────────────
# #         all_countries = sorted(df["Country"].unique().tolist())
# #         selected_countries = st.multiselect(
# #             "Countries",
# #             options=all_countries,
# #             default=st.session_state["filter_countries"],
# #             key="_countries_widget",
# #         )
# #         st.session_state["filter_countries"] = selected_countries if selected_countries else all_countries

# #         # ── Seating Region ────────────────────────────────────────────────
# #         all_seating = sorted(df["Seating_Region"].unique().tolist())
# #         selected_seating = st.multiselect(
# #             "Seating Region",
# #             options=all_seating,
# #             default=st.session_state["filter_seating"],
# #             key="_seating_widget",
# #         )
# #         st.session_state["filter_seating"] = selected_seating if selected_seating else all_seating

# #         # ── Gender ────────────────────────────────────────────────────────
# #         all_genders = sorted(df["Gender"].unique().tolist())
# #         selected_genders = st.multiselect(
# #             "Gender",
# #             options=all_genders,
# #             default=st.session_state["filter_gender"],
# #             key="_gender_widget",
# #         )
# #         st.session_state["filter_gender"] = selected_genders if selected_genders else all_genders

# #         # ── Age Group ─────────────────────────────────────────────────────
# #         all_age_groups = sorted(
# #             df["Age_Group"].unique().tolist(),
# #             key=lambda x: int(x.split("-")[0].replace("+", "").strip()),
# #         )
# #         selected_age_groups = st.multiselect(
# #             "Age Group",
# #             options=all_age_groups,
# #             default=st.session_state["filter_age_groups"],
# #             key="_age_groups_widget",
# #         )
# #         st.session_state["filter_age_groups"] = selected_age_groups if selected_age_groups else all_age_groups

# #         # ── Visit Type ────────────────────────────────────────────────────
# #         visit_type = st.radio(
# #             "Visit Type",
# #             options=["All", "First-time", "Repeat"],
# #             index=["All", "First-time", "Repeat"].index(st.session_state["filter_visit_type"]),
# #             key="_visit_type_widget",
# #             horizontal=True,
# #         )
# #         st.session_state["filter_visit_type"] = visit_type

# #         st.markdown("---")

# #         # Reset button
# #         if st.button("Reset Filters", use_container_width=True):
# #             for key in list(st.session_state.keys()):
# #                 if key.startswith("filter_"):
# #                     del st.session_state[key]
# #             st.rerun()

# #         # ── Stats ─────────────────────────────────────────────────────────
# #         st.markdown("### Dataset")
# #         st.caption(f"Total records: **{len(df):,}**")

# #     # ── Apply Filters ─────────────────────────────────────────────────────
# #     date_start, date_end = st.session_state["filter_date_range"]
# #     mask = (
# #         (df["Visit_Date"].dt.date >= date_start)
# #         & (df["Visit_Date"].dt.date <= date_end)
# #         & (df["Country"].isin(st.session_state["filter_countries"]))
# #         & (df["Seating_Region"].isin(st.session_state["filter_seating"]))
# #         & (df["Gender"].isin(st.session_state["filter_gender"]))
# #         & (df["Age_Group"].isin(st.session_state["filter_age_groups"]))
# #     )
# #     if st.session_state["filter_visit_type"] != "All":
# #         mask &= df["Visit_Type"] == st.session_state["filter_visit_type"]

# #     filtered = df[mask].copy()

# #     # Show filtered count in sidebar
# #     with st.sidebar:
# #         st.caption(f"Filtered records: **{len(filtered):,}**")

# #     return filtered

# import pandas as pd
# import streamlit as st

# from src.data_prep import prepare_data
# from src.styles import inject_css


# def _init_filters(df: pd.DataFrame):
#     """Initialize session_state filter defaults if not set."""
#     if "filter_initialized" not in st.session_state:
#         min_date = df["Visit_Date"].min().date()
#         max_date = df["Visit_Date"].max().date()

#         st.session_state["filter_date_range"] = (min_date, max_date)
#         st.session_state["filter_countries"] = sorted(df["Country"].unique().tolist())
#         st.session_state["filter_seating"] = sorted(df["Seating_Region"].unique().tolist())
#         st.session_state["filter_gender"] = sorted(df["Gender"].unique().tolist())
#         st.session_state["filter_age_groups"] = sorted(
#             df["Age_Group"].unique().tolist(),
#             key=lambda x: int(x.split("-")[0].replace("+", "").strip()),
#         )
#         st.session_state["filter_visit_type"] = "All"
#         st.session_state["filter_initialized"] = True


# def render_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
#     """Render sidebar filters and return the filtered DataFrame."""
#     _init_filters(df)

#     with st.sidebar:
#         st.markdown("## Filters")
#         st.markdown("---")

#         # ── Date Range ────────────────────────────────────────────────────
#         min_date = df["Visit_Date"].min().date()
#         max_date = df["Visit_Date"].max().date()

#         st.markdown("**Date Range**")
#         date_range = st.date_input(
#             "Select date range",
#             value=st.session_state["filter_date_range"],
#             min_value=min_date,
#             max_value=max_date,
#             key="_date_range_widget",
#             label_visibility="collapsed",
#         )
#         if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
#             st.session_state["filter_date_range"] = (date_range[0], date_range[1])
#         elif isinstance(date_range, (list, tuple)) and len(date_range) == 1:
#             st.session_state["filter_date_range"] = (date_range[0], max_date)

#         st.markdown("---")

#         # ── Country ───────────────────────────────────────────────────────
#         all_countries = sorted(df["Country"].unique().tolist())
#         st.markdown("**Countries**")
#         selected_countries = st.pills(
#             "Countries",
#             options=all_countries,
#             default=st.session_state["filter_countries"],
#             selection_mode="multi",
#             key="_countries_widget",
#             label_visibility="collapsed"
#         )
#         st.session_state["filter_countries"] = selected_countries if selected_countries else all_countries

#         # ── Seating Region ────────────────────────────────────────────────
#         all_seating = sorted(df["Seating_Region"].unique().tolist())
#         st.markdown("**Seating Region**")
#         selected_seating = st.pills(
#             "Seating Region",
#             options=all_seating,
#             default=st.session_state["filter_seating"],
#             selection_mode="multi",
#             key="_seating_widget",
#             label_visibility="collapsed"
#         )
#         st.session_state["filter_seating"] = selected_seating if selected_seating else all_seating

#         # ── Gender ────────────────────────────────────────────────────────
#         all_genders = sorted(df["Gender"].unique().tolist())
#         st.markdown("**Gender**")
#         selected_genders = st.pills(
#             "Gender",
#             options=all_genders,
#             default=st.session_state["filter_gender"],
#             selection_mode="multi",
#             key="_gender_widget",
#             label_visibility="collapsed"
#         )
#         st.session_state["filter_gender"] = selected_genders if selected_genders else all_genders

#         # ── Age Group ─────────────────────────────────────────────────────
#         all_age_groups = sorted(
#             df["Age_Group"].unique().tolist(),
#             key=lambda x: int(x.split("-")[0].replace("+", "").strip()),
#         )
#         st.markdown("**Age Group**")
#         selected_age_groups = st.pills(
#             "Age Group",
#             options=all_age_groups,
#             default=st.session_state["filter_age_groups"],
#             selection_mode="multi",
#             key="_age_groups_widget",
#             label_visibility="collapsed"
#         )
#         st.session_state["filter_age_groups"] = selected_age_groups if selected_age_groups else all_age_groups

#         # ── Visit Type ────────────────────────────────────────────────────
#         st.markdown("**Visit Type**")
#         visit_type = st.pills(
#             "Visit Type",
#             options=["All", "First-time", "Repeat"],
#             default=st.session_state["filter_visit_type"],
#             selection_mode="single",
#             key="_visit_type_widget",
#             label_visibility="collapsed"
#         )
#         # Fallback to "All" if user accidentally clicks to deselect the active pill
#         st.session_state["filter_visit_type"] = visit_type if visit_type else "All"

#         st.markdown("---")

#         # Reset button
#         if st.button("Reset Filters", use_container_width=True):
#             for key in list(st.session_state.keys()):
#                 if key.startswith("filter_"):
#                     del st.session_state[key]
#             st.rerun()

#         # ── Stats ─────────────────────────────────────────────────────────
#         st.markdown("### Dataset")
#         st.caption(f"Total records: **{len(df):,}**")

#     # ── Apply Filters ─────────────────────────────────────────────────────
#     date_start, date_end = st.session_state["filter_date_range"]
#     mask = (
#         (df["Visit_Date"].dt.date >= date_start)
#         & (df["Visit_Date"].dt.date <= date_end)
#         & (df["Country"].isin(st.session_state["filter_countries"]))
#         & (df["Seating_Region"].isin(st.session_state["filter_seating"]))
#         & (df["Gender"].isin(st.session_state["filter_gender"]))
#         & (df["Age_Group"].isin(st.session_state["filter_age_groups"]))
#     )
#     if st.session_state["filter_visit_type"] != "All":
#         mask &= df["Visit_Type"] == st.session_state["filter_visit_type"]

#     filtered = df[mask].copy()

#     # Show filtered count in sidebar
#     with st.sidebar:
#         st.caption(f"Filtered records: **{len(filtered):,}**")

#     return filtered

import pandas as pd
import streamlit as st

from src.data_prep import prepare_data
from src.styles import inject_css


def _pill_callback(widget_key: str):
    """Callback to handle mutual exclusivity of 'All' in multi-select pills."""
    current = st.session_state[widget_key]
    prev_key = f"{widget_key}_prev"
    prev = st.session_state.get(prev_key, ["All"])
    
    if "All" in current and "All" not in prev:
        # User just selected "All" -> clear everything else
        st.session_state[widget_key] = ["All"]
    elif "All" in current and len(current) > 1:
        # User selected another option while "All" was active -> remove "All"
        current.remove("All")
        st.session_state[widget_key] = current
    elif not current:
        # User deselected all options -> default back to "All"
        st.session_state[widget_key] = ["All"]
        
    st.session_state[prev_key] = st.session_state[widget_key].copy()


def _init_filters(df: pd.DataFrame):
    """Initialize session_state filter defaults if not set."""
    if "filter_initialized" not in st.session_state:
        min_date = df["Visit_Date"].min().date()
        max_date = df["Visit_Date"].max().date()

        st.session_state["filter_date_range"] = (min_date, max_date)
        
        # Initialize logical filter states
        st.session_state["filter_countries"] = sorted(df["Country"].unique().tolist())
        st.session_state["filter_seating"] = sorted(df["Seating_Region"].unique().tolist())
        st.session_state["filter_gender"] = sorted(df["Gender"].unique().tolist())
        st.session_state["filter_age_groups"] = sorted(
            df["Age_Group"].unique().tolist(),
            key=lambda x: int(x.split("-")[0].replace("+", "").strip()),
        )
        st.session_state["filter_visit_type"] = "All"
        
        # Initialize widget UI states for pills
        for w in ["_countries_widget", "_seating_widget", "_gender_widget", "_age_groups_widget"]:
            st.session_state[w] = ["All"]
            st.session_state[f"{w}_prev"] = ["All"]

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
        st.markdown("**Countries**")
        st.pills(
            "Countries",
            options=["All"] + all_countries,
            selection_mode="multi",
            key="_countries_widget",
            on_change=_pill_callback,
            args=("_countries_widget",),
            label_visibility="collapsed"
        )
        st.session_state["filter_countries"] = all_countries if "All" in st.session_state["_countries_widget"] else st.session_state["_countries_widget"]

        # ── Seating Region ────────────────────────────────────────────────
        all_seating = sorted(df["Seating_Region"].unique().tolist())
        st.markdown("**Seating Region**")
        st.pills(
            "Seating Region",
            options=["All"] + all_seating,
            selection_mode="multi",
            key="_seating_widget",
            on_change=_pill_callback,
            args=("_seating_widget",),
            label_visibility="collapsed"
        )
        st.session_state["filter_seating"] = all_seating if "All" in st.session_state["_seating_widget"] else st.session_state["_seating_widget"]

        # ── Gender ────────────────────────────────────────────────────────
        all_genders = sorted(df["Gender"].unique().tolist())
        st.markdown("**Gender**")
        st.pills(
            "Gender",
            options=["All"] + all_genders,
            selection_mode="multi",
            key="_gender_widget",
            on_change=_pill_callback,
            args=("_gender_widget",),
            label_visibility="collapsed"
        )
        st.session_state["filter_gender"] = all_genders if "All" in st.session_state["_gender_widget"] else st.session_state["_gender_widget"]

        # ── Age Group ─────────────────────────────────────────────────────
        all_age_groups = sorted(
            df["Age_Group"].unique().tolist(),
            key=lambda x: int(x.split("-")[0].replace("+", "").strip()),
        )
        st.markdown("**Age Group**")
        st.pills(
            "Age Group",
            options=["All"] + all_age_groups,
            selection_mode="multi",
            key="_age_groups_widget",
            on_change=_pill_callback,
            args=("_age_groups_widget",),
            label_visibility="collapsed"
        )
        st.session_state["filter_age_groups"] = all_age_groups if "All" in st.session_state["_age_groups_widget"] else st.session_state["_age_groups_widget"]

        # ── Visit Type ────────────────────────────────────────────────────
        st.markdown("**Visit Type**")
        visit_type = st.pills(
            "Visit Type",
            options=["All", "First-time", "Repeat"],
            default=st.session_state["filter_visit_type"],
            selection_mode="single",
            key="_visit_type_widget",
            label_visibility="collapsed"
        )
        # Fallback to "All" if user accidentally clicks to deselect the active pill
        st.session_state["filter_visit_type"] = visit_type if visit_type else "All"

        st.markdown("---")

        # Reset button
        if st.button("Reset Filters", use_container_width=True):
            keys_to_delete = [
                k for k in st.session_state.keys()
                if k.startswith("filter_") or 
                   k.startswith("_countries_widget") or 
                   k.startswith("_seating_widget") or 
                   k.startswith("_gender_widget") or 
                   k.startswith("_age_groups_widget")
            ]
            for key in keys_to_delete:
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