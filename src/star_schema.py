import pandas as pd
import streamlit as st

from src.data_prep import prepare_data

COUNTRY_CONTINENT = {
    "Australia": "Oceania",
    "France": "Europe",
    "Germany": "Europe",
    "Japan": "Asia",
    "Sweden": "Europe",
    "UK": "Europe",
    "USA": "North America",
}

COUNTRY_ISO3 = {
    "Australia": "AUS",
    "France": "FRA",
    "Germany": "DEU",
    "Japan": "JPN",
    "Sweden": "SWE",
    "UK": "GBR",
    "USA": "USA",
}


@st.cache_data(show_spinner=False)
def build_star_schema():
    """Build star schema tables from the prepared dataset."""
    df = prepare_data()

    # ── dim_customer ───────────────────────────────────────────────────────
    dim_customer = (
        df[["Customer_ID", "Age", "Gender", "Age_Group", "Spend_Tier"]]
        .drop_duplicates(subset="Customer_ID")
        .reset_index(drop=True)
    )

    # ── dim_date ───────────────────────────────────────────────────────────
    dates = df["Visit_Date"].drop_duplicates().sort_values().reset_index(drop=True)
    dim_date = pd.DataFrame({
        "Date_Key": range(1, len(dates) + 1),
        "Visit_Date": dates,
        "Day": dates.dt.day,
        "Month": dates.dt.month,
        "Month_Name": dates.dt.strftime("%B"),
        "Quarter": dates.dt.quarter,
        "Year": dates.dt.year,
        "Day_of_Week": dates.dt.day_name(),
        "Week_Number": dates.dt.isocalendar().week.astype(int),
    })
    date_key_map = dict(zip(dim_date["Visit_Date"], dim_date["Date_Key"]))

    # ── dim_seating ────────────────────────────────────────────────────────
    seating_df = (
        df[["Seating_Region", "Ticket_Price"]]
        .drop_duplicates(subset="Seating_Region")
        .sort_values("Ticket_Price", ascending=False)
        .reset_index(drop=True)
    )
    seating_df.insert(0, "Seating_Key", range(1, len(seating_df) + 1))
    dim_seating = seating_df
    seating_key_map = dict(zip(dim_seating["Seating_Region"], dim_seating["Seating_Key"]))

    # ── dim_geography ──────────────────────────────────────────────────────
    countries = df["Country"].drop_duplicates().sort_values().reset_index(drop=True)
    dim_geography = pd.DataFrame({
        "Country_Key": range(1, len(countries) + 1),
        "Country": countries,
        "Continent": countries.map(COUNTRY_CONTINENT),
        "ISO3": countries.map(COUNTRY_ISO3),
    })
    country_key_map = dict(zip(dim_geography["Country"], dim_geography["Country_Key"]))

    # ── fact_transactions ──────────────────────────────────────────────────
    fact_transactions = df[[
        "Customer_ID", "Visit_Date", "Seating_Region", "Country",
        "Ticket_Revenue", "Merchandise_Spend", "Drink_Spend", "Total_Spend",
        "Num_Tickets", "Repeat_Visit", "Satisfaction_Score", "Recommendation_Likelihood",
    ]].copy()

    fact_transactions["Date_Key"] = fact_transactions["Visit_Date"].map(date_key_map)
    fact_transactions["Seating_Key"] = fact_transactions["Seating_Region"].map(seating_key_map)
    fact_transactions["Country_Key"] = fact_transactions["Country"].map(country_key_map)
    fact_transactions = fact_transactions.drop(columns=["Visit_Date", "Seating_Region", "Country"])

    return {
        "fact_transactions": fact_transactions,
        "dim_customer": dim_customer,
        "dim_date": dim_date,
        "dim_seating": dim_seating,
        "dim_geography": dim_geography,
    }
