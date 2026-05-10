import pandas as pd
import numpy as np
import streamlit as st

from src.data_loader import load_raw_data


@st.cache_data(show_spinner=False)
def prepare_data() -> pd.DataFrame:
    """Clean, cast types, and add derived columns to the raw dataset."""
    df = load_raw_data().copy()

    # ── Type Casting ───────────────────────────────────────────────────────
    df["Visit_Date"] = pd.to_datetime(df["Visit_Date"])
    df["Age"] = df["Age"].astype(int)
    df["Num_Tickets"] = df["Num_Tickets"].astype(int)
    df["Repeat_Visit"] = df["Repeat_Visit"].astype(int)
    df["Ticket_Price"] = df["Ticket_Price"].astype(float)
    df["Merchandise_Spend"] = df["Merchandise_Spend"].astype(float)
    df["Drink_Spend"] = df["Drink_Spend"].astype(float)
    df["Satisfaction_Score"] = df["Satisfaction_Score"].astype(float)
    df["Recommendation_Likelihood"] = df["Recommendation_Likelihood"].astype(float)

    # ── Derived Columns ────────────────────────────────────────────────────
    df["Ticket_Revenue"] = df["Ticket_Price"] * df["Num_Tickets"]
    df["Total_Spend"] = df["Ticket_Revenue"] + df["Merchandise_Spend"] + df["Drink_Spend"]

    df["Month_Label"] = df["Visit_Date"].dt.strftime("%b %Y")
    df["Month_Num"] = df["Visit_Date"].dt.to_period("M")
    df["Visit_Quarter"] = "Q" + df["Visit_Date"].dt.quarter.astype(str) + " " + df["Visit_Date"].dt.year.astype(str)

    df["Age_Group"] = pd.cut(
        df["Age"],
        bins=[17, 25, 35, 45, 55, 65, 200],
        labels=["18-25", "26-35", "36-45", "46-55", "56-65", "66+"],
    )
    df["Age_Group"] = df["Age_Group"].astype(str)

    df["Visit_Type"] = df["Repeat_Visit"].map({1: "Repeat", 0: "First-time"})

    spend_quartiles = df["Total_Spend"].quantile([0.25, 0.50, 0.75])
    df["Spend_Tier"] = pd.cut(
        df["Total_Spend"],
        bins=[-np.inf, spend_quartiles[0.25], spend_quartiles[0.50], spend_quartiles[0.75], np.inf],
        labels=["Low", "Medium", "High", "Premium"],
    )
    df["Spend_Tier"] = df["Spend_Tier"].astype(str)

    # Sort by date for time-based analysis
    df = df.sort_values("Visit_Date").reset_index(drop=True)

    return df
