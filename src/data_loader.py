import os
import pandas as pd
import streamlit as st


DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "Company_X_Audience.csv")


@st.cache_data(show_spinner=False)
def load_raw_data() -> pd.DataFrame:
    """Load the raw CSV dataset. Cached for performance."""
    return pd.read_csv(DATA_PATH)
