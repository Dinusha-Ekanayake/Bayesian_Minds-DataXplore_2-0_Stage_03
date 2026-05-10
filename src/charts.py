"""
Plotly figure factory functions for all dashboard charts.
Each function accepts a filtered DataFrame and returns a go.Figure / px Figure.
"""
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.styles import (
    PLOTLY_LAYOUT,
    SEATING_COLORS,
    GENDER_COLORS,
    REVENUE_STREAM_COLORS,
    COUNTRY_COLORS,
    AGE_GROUP_COLORS,
)

SEATING_ORDER = ["VIP", "Premium", "High Economy", "Economy"]
AGE_GROUP_ORDER = ["18-25", "26-35", "36-45", "46-55", "56-65", "66+"]
SPEND_TIER_ORDER = ["Low", "Medium", "High", "Premium"]


def _apply_layout(fig, title: str = "") -> go.Figure:
    fig.update_layout(**PLOTLY_LAYOUT)
    if title:
        fig.update_layout(title=dict(text=title, font=dict(size=16, color="#FAFAFA")))
    return fig


# ══════════════════════════════════════════════════════════════════════════════
#  REVENUE ANALYSIS CHARTS
# ══════════════════════════════════════════════════════════════════════════════

def fig_revenue_by_seating(df: pd.DataFrame) -> go.Figure:
    """Stacked bar: Ticket / Merch / Drink revenue by Seating Region."""
    grp = (
        df.groupby("Seating_Region")[["Ticket_Revenue", "Merchandise_Spend", "Drink_Spend"]]
        .sum()
        .reindex([s for s in SEATING_ORDER if s in df["Seating_Region"].unique()])
        .reset_index()
    )
    fig = go.Figure()
    for col, color, label in [
        ("Ticket_Revenue", "#FF6B6B", "Ticket Revenue"),
        ("Merchandise_Spend", "#4ECDC4", "Merchandise"),
        ("Drink_Spend", "#FFE66D", "Drinks"),
    ]:
        fig.add_trace(go.Bar(
            name=label,
            x=grp["Seating_Region"],
            y=grp[col],
            marker_color=color,
            hovertemplate=f"<b>%{{x}}</b><br>{label}: $%{{y:,.0f}}<extra></extra>",
        ))
    fig.update_layout(barmode="stack")
    return _apply_layout(fig, "Revenue by Seating Region")


def fig_revenue_by_country(df: pd.DataFrame) -> go.Figure:
    """Grouped bar: revenue streams by country."""
    grp = (
        df.groupby("Country")[["Ticket_Revenue", "Merchandise_Spend", "Drink_Spend"]]
        .sum()
        .sort_values("Ticket_Revenue", ascending=False)
        .reset_index()
    )
    fig = go.Figure()
    for col, color, label in [
        ("Ticket_Revenue", "#FF6B6B", "Ticket Revenue"),
        ("Merchandise_Spend", "#4ECDC4", "Merchandise"),
        ("Drink_Spend", "#FFE66D", "Drinks"),
    ]:
        fig.add_trace(go.Bar(
            name=label,
            x=grp["Country"],
            y=grp[col],
            marker_color=color,
            hovertemplate=f"<b>%{{x}}</b><br>{label}: $%{{y:,.0f}}<extra></extra>",
        ))
    fig.update_layout(barmode="group")
    return _apply_layout(fig, "Revenue by Country")


def fig_treemap_country_region(df: pd.DataFrame) -> go.Figure:
    """Treemap: Total spend by Country > Seating Region."""
    grp = df.groupby(["Country", "Seating_Region"])["Total_Spend"].sum().reset_index()
    fig = px.treemap(
        grp,
        path=["Country", "Seating_Region"],
        values="Total_Spend",
        color="Country",
        color_discrete_map=COUNTRY_COLORS,
        hover_data={"Total_Spend": ":,.0f"},
    )
    fig.update_traces(textinfo="label+percent parent", hovertemplate="<b>%{label}</b><br>Revenue: $%{value:,.0f}<extra></extra>")
    return _apply_layout(fig, "Revenue by Country & Seating Region")


def fig_revenue_by_age_group(df: pd.DataFrame) -> go.Figure:
    """Horizontal bar: revenue by age group, colored by visit type."""
    grp = (
        df.groupby(["Age_Group", "Visit_Type"])["Total_Spend"]
        .sum()
        .reset_index()
    )
    present = [g for g in AGE_GROUP_ORDER if g in grp["Age_Group"].unique()]
    fig = px.bar(
        grp,
        y="Age_Group",
        x="Total_Spend",
        color="Visit_Type",
        color_discrete_map={"Repeat": "#4A9EFF", "First-time": "#FF6B9D"},
        category_orders={"Age_Group": list(reversed(present))},
        orientation="h",
        barmode="stack",
        labels={"Total_Spend": "Total Revenue ($)", "Age_Group": "Age Group"},
    )
    fig.update_traces(hovertemplate="<b>%{y}</b><br>Revenue: $%{x:,.0f}<extra></extra>")
    return _apply_layout(fig, "Revenue by Age Group & Visit Type")


def fig_sunburst_revenue(df: pd.DataFrame) -> go.Figure:
    """Sunburst: Country > Seating > Gender revenue drill-down."""
    grp = df.groupby(["Country", "Seating_Region", "Gender"])["Total_Spend"].sum().reset_index()
    fig = px.sunburst(
        grp,
        path=["Country", "Seating_Region", "Gender"],
        values="Total_Spend",
        color="Country",
        color_discrete_map=COUNTRY_COLORS,
    )
    fig.update_traces(hovertemplate="<b>%{label}</b><br>Revenue: $%{value:,.0f}<extra></extra>")
    return _apply_layout(fig, "Revenue Hierarchy: Country → Seating → Gender")


# ══════════════════════════════════════════════════════════════════════════════
#  CUSTOMER ANALYSIS CHARTS
# ══════════════════════════════════════════════════════════════════════════════

def fig_gender_donut(df: pd.DataFrame) -> go.Figure:
    """Donut chart: gender distribution."""
    counts = df["Gender"].value_counts().reset_index()
    counts.columns = ["Gender", "Count"]
    fig = px.pie(
        counts,
        names="Gender",
        values="Count",
        hole=0.55,
        color="Gender",
        color_discrete_map=GENDER_COLORS,
    )
    fig.update_traces(hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Share: %{percent}<extra></extra>")
    return _apply_layout(fig, "Gender Distribution")


def fig_seating_donut(df: pd.DataFrame) -> go.Figure:
    """Donut chart: seating region distribution."""
    counts = df["Seating_Region"].value_counts().reset_index()
    counts.columns = ["Seating_Region", "Count"]
    fig = px.pie(
        counts,
        names="Seating_Region",
        values="Count",
        hole=0.55,
        color="Seating_Region",
        color_discrete_map=SEATING_COLORS,
    )
    fig.update_traces(hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Share: %{percent}<extra></extra>")
    return _apply_layout(fig, "Seating Region Distribution")


def fig_age_histogram(df: pd.DataFrame) -> go.Figure:
    """Histogram: age distribution by gender."""
    fig = px.histogram(
        df,
        x="Age",
        color="Gender",
        nbins=25,
        color_discrete_map=GENDER_COLORS,
        barmode="overlay",
        opacity=0.75,
        labels={"Age": "Age", "count": "Customers"},
    )
    fig.update_traces(hovertemplate="Age: %{x}<br>Count: %{y}<extra></extra>")
    return _apply_layout(fig, "Age Distribution by Gender")


def fig_choropleth(df: pd.DataFrame) -> go.Figure:
    """Choropleth: customer count by country."""
    from src.star_schema import COUNTRY_ISO3
    grp = df.groupby("Country")["Customer_ID"].count().reset_index()
    grp.columns = ["Country", "Customers"]
    grp["ISO3"] = grp["Country"].map(COUNTRY_ISO3)
    fig = px.choropleth(
        grp,
        locations="ISO3",
        color="Customers",
        hover_name="Country",
        color_continuous_scale=[[0, "#1A1F2E"], [0.5, "#7B68EE"], [1, "#FFD700"]],
        labels={"Customers": "Customer Count"},
    )
    fig.update_layout(
        geo=dict(
            bgcolor="rgba(0,0,0,0)",
            showframe=False,
            showcoastlines=True,
            coastlinecolor="rgba(255,255,255,0.2)",
            landcolor="#1A1F2E",
            oceancolor="#0E1117",
            showocean=True,
        )
    )
    return _apply_layout(fig, "Geographic Distribution of Customers")


def fig_spend_boxplot(df: pd.DataFrame) -> go.Figure:
    """Box plot: total spend distribution by seating region."""
    present = [s for s in SEATING_ORDER if s in df["Seating_Region"].unique()]
    fig = px.box(
        df,
        x="Seating_Region",
        y="Total_Spend",
        color="Seating_Region",
        color_discrete_map=SEATING_COLORS,
        category_orders={"Seating_Region": present},
        labels={"Total_Spend": "Total Spend ($)", "Seating_Region": "Seating Region"},
    )
    fig.update_traces(hovertemplate="<b>%{x}</b><br>Spend: $%{y:,.0f}<extra></extra>")
    return _apply_layout(fig, "Spend Distribution by Seating Region")


def fig_repeat_vs_firsttime_spend(df: pd.DataFrame) -> go.Figure:
    """Grouped bar: avg spend by visit type and seating region."""
    grp = (
        df.groupby(["Seating_Region", "Visit_Type"])["Total_Spend"]
        .mean()
        .reset_index()
    )
    present = [s for s in SEATING_ORDER if s in grp["Seating_Region"].unique()]
    fig = px.bar(
        grp,
        x="Seating_Region",
        y="Total_Spend",
        color="Visit_Type",
        barmode="group",
        color_discrete_map={"Repeat": "#4A9EFF", "First-time": "#FF6B9D"},
        category_orders={"Seating_Region": present},
        labels={"Total_Spend": "Avg Spend ($)", "Seating_Region": "Seating Region"},
    )
    fig.update_traces(hovertemplate="<b>%{x}</b><br>Avg Spend: $%{y:,.0f}<extra></extra>")
    return _apply_layout(fig, "Avg Spend: Repeat vs First-time Visitors")


def fig_age_vs_spend_scatter(df: pd.DataFrame) -> go.Figure:
    """Scatter: Age vs Total Spend, colored by region, sized by tickets."""
    fig = px.scatter(
        df,
        x="Age",
        y="Total_Spend",
        color="Seating_Region",
        size="Num_Tickets",
        color_discrete_map=SEATING_COLORS,
        opacity=0.7,
        labels={"Total_Spend": "Total Spend ($)", "Age": "Age"},
        hover_data={"Customer_ID": True, "Gender": True, "Country": True},
    )
    return _apply_layout(fig, "Age vs Total Spend (size = tickets, color = region)")


# ══════════════════════════════════════════════════════════════════════════════
#  EXPERIENCE ANALYSIS CHARTS
# ══════════════════════════════════════════════════════════════════════════════

def fig_satisfaction_by_region_visittype(df: pd.DataFrame) -> go.Figure:
    """Grouped bar: avg satisfaction by seating region & visit type."""
    grp = (
        df.groupby(["Seating_Region", "Visit_Type"])["Satisfaction_Score"]
        .mean()
        .reset_index()
    )
    present = [s for s in SEATING_ORDER if s in grp["Seating_Region"].unique()]
    fig = px.bar(
        grp,
        x="Seating_Region",
        y="Satisfaction_Score",
        color="Visit_Type",
        barmode="group",
        color_discrete_map={"Repeat": "#4A9EFF", "First-time": "#FF6B9D"},
        category_orders={"Seating_Region": present},
        labels={"Satisfaction_Score": "Avg Satisfaction (0-10)"},
    )
    fig.update_layout(yaxis=dict(range=[0, 10]))
    return _apply_layout(fig, "Satisfaction by Region & Visit Type")


def fig_recommendation_by_country(df: pd.DataFrame) -> go.Figure:
    """Grouped bar: avg recommendation by country & visit type."""
    grp = (
        df.groupby(["Country", "Visit_Type"])["Recommendation_Likelihood"]
        .mean()
        .reset_index()
        .sort_values("Recommendation_Likelihood", ascending=False)
    )
    fig = px.bar(
        grp,
        x="Country",
        y="Recommendation_Likelihood",
        color="Visit_Type",
        barmode="group",
        color_discrete_map={"Repeat": "#4A9EFF", "First-time": "#FF6B9D"},
        labels={"Recommendation_Likelihood": "Avg Recommendation (0-10)"},
    )
    fig.update_layout(yaxis=dict(range=[0, 10]))
    return _apply_layout(fig, "Recommendation Likelihood by Country & Visit Type")


def fig_spend_vs_satisfaction(df: pd.DataFrame) -> go.Figure:
    """Scatter with OLS trendline: Total Spend vs Satisfaction."""
    fig = px.scatter(
        df,
        x="Total_Spend",
        y="Satisfaction_Score",
        trendline="ols",
        color="Seating_Region",
        color_discrete_map=SEATING_COLORS,
        opacity=0.6,
        labels={"Total_Spend": "Total Spend ($)", "Satisfaction_Score": "Satisfaction Score"},
    )
    return _apply_layout(fig, "Spend vs Satisfaction Score")


def fig_spend_vs_recommendation(df: pd.DataFrame) -> go.Figure:
    """Scatter with OLS trendline: Total Spend vs Recommendation."""
    fig = px.scatter(
        df,
        x="Total_Spend",
        y="Recommendation_Likelihood",
        trendline="ols",
        color="Seating_Region",
        color_discrete_map=SEATING_COLORS,
        opacity=0.6,
        labels={"Total_Spend": "Total Spend ($)", "Recommendation_Likelihood": "Recommendation Likelihood"},
    )
    return _apply_layout(fig, "Spend vs Recommendation Likelihood")


def fig_correlation_heatmap(df: pd.DataFrame) -> go.Figure:
    """Heatmap: correlation matrix of numeric columns."""
    cols = ["Age", "Ticket_Price", "Num_Tickets", "Merchandise_Spend",
            "Drink_Spend", "Ticket_Revenue", "Total_Spend",
            "Satisfaction_Score", "Recommendation_Likelihood"]
    corr = df[cols].corr()
    fig = go.Figure(go.Heatmap(
        z=corr.values,
        x=corr.columns.tolist(),
        y=corr.columns.tolist(),
        colorscale=[
            [0, "#FF6B6B"], [0.5, "#1A1F2E"], [1, "#4A9EFF"]
        ],
        zmid=0,
        text=np.round(corr.values, 2),
        texttemplate="%{text}",
        hovertemplate="<b>%{x}</b> vs <b>%{y}</b><br>Correlation: %{z:.3f}<extra></extra>",
    ))
    fig.update_layout(
        xaxis=dict(tickangle=-35, tickfont=dict(size=10)),
        yaxis=dict(tickfont=dict(size=10)),
    )
    return _apply_layout(fig, "Correlation Matrix")


def fig_satisfaction_violin(df: pd.DataFrame) -> go.Figure:
    """Violin plot: satisfaction score distribution by seating region."""
    present = [s for s in SEATING_ORDER if s in df["Seating_Region"].unique()]
    fig = go.Figure()
    for region in present:
        subset = df[df["Seating_Region"] == region]["Satisfaction_Score"]
        fig.add_trace(go.Violin(
            y=subset,
            name=region,
            box_visible=True,
            meanline_visible=True,
            fillcolor=SEATING_COLORS.get(region, "#AAAAAA"),
            opacity=0.8,
            line_color="rgba(255,255,255,0.5)",
        ))
    fig.update_layout(showlegend=False, yaxis_title="Satisfaction Score")
    return _apply_layout(fig, "Satisfaction Distribution by Seating Region")


def fig_radar_country_comparison(df: pd.DataFrame) -> go.Figure:
    """Radar chart: avg Satisfaction & Recommendation by country."""
    grp = (
        df.groupby("Country")[["Satisfaction_Score", "Recommendation_Likelihood", "Total_Spend"]]
        .mean()
        .reset_index()
    )
    # Normalize Total_Spend to 0-10 scale
    ts_min, ts_max = grp["Total_Spend"].min(), grp["Total_Spend"].max()
    if ts_max > ts_min:
        grp["Spend_Norm"] = (grp["Total_Spend"] - ts_min) / (ts_max - ts_min) * 10
    else:
        grp["Spend_Norm"] = 5.0

    categories = ["Satisfaction", "Recommendation", "Avg Spend (norm)"]
    fig = go.Figure()
    colors = ["#FF6B6B", "#4A9EFF", "#FFE66D", "#50E3C2", "#FF6B9D", "#7B68EE", "#FFD700"]
    for i, row in grp.iterrows():
        values = [
            row["Satisfaction_Score"],
            row["Recommendation_Likelihood"],
            row["Spend_Norm"],
        ]
        values_closed = values + [values[0]]
        cats_closed = categories + [categories[0]]
        fig.add_trace(go.Scatterpolar(
            r=values_closed,
            theta=cats_closed,
            fill="toself",
            name=row["Country"],
            opacity=0.6,
            line=dict(color=colors[i % len(colors)]),
        ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(26,31,46,0.6)",
            radialaxis=dict(visible=True, range=[0, 10], color="#9CA3AF"),
            angularaxis=dict(color="#9CA3AF"),
        )
    )
    return _apply_layout(fig, "Country Comparison: Satisfaction, Recommendation & Spend")


# ══════════════════════════════════════════════════════════════════════════════
#  TIME-BASED ANALYSIS CHARTS
# ══════════════════════════════════════════════════════════════════════════════

def _monthly_df(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate metrics by month, returning sorted months."""
    grp = (
        df.groupby("Month_Label")
        .agg(
            Total_Revenue=("Total_Spend", "sum"),
            Ticket_Revenue=("Ticket_Revenue", "sum"),
            Merch_Revenue=("Merchandise_Spend", "sum"),
            Drink_Revenue=("Drink_Spend", "sum"),
            Customers=("Customer_ID", "count"),
            Avg_Satisfaction=("Satisfaction_Score", "mean"),
            Repeat_Count=("Repeat_Visit", "sum"),
            Month_Num=("Month_Num", "first"),
        )
        .reset_index()
        .sort_values("Month_Num")
    )
    grp["Repeat_Rate"] = grp["Repeat_Count"] / grp["Customers"] * 100
    return grp


def fig_monthly_revenue_trend(df: pd.DataFrame) -> go.Figure:
    """Area line chart: total revenue trend by month."""
    mdf = _monthly_df(df)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=mdf["Month_Label"],
        y=mdf["Total_Revenue"],
        mode="lines+markers",
        fill="tozeroy",
        fillcolor="rgba(255,107,107,0.15)",
        line=dict(color="#FF6B6B", width=2.5),
        marker=dict(size=7, color="#FF6B6B"),
        hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>",
        name="Total Revenue",
    ))
    fig.update_layout(xaxis_title="Month", yaxis_title="Revenue ($)")
    return _apply_layout(fig, "Monthly Revenue Trend")


def fig_monthly_revenue_streams(df: pd.DataFrame) -> go.Figure:
    """Stacked area: Ticket / Merch / Drink by month."""
    mdf = _monthly_df(df)
    fig = go.Figure()
    stream_info = [
        ("Drink_Revenue", "#FFE66D", "Drinks"),
        ("Merch_Revenue", "#4ECDC4", "Merchandise"),
        ("Ticket_Revenue", "#FF6B6B", "Tickets"),
    ]
    for col, color, name in stream_info:
        fig.add_trace(go.Scatter(
            x=mdf["Month_Label"],
            y=mdf[col],
            mode="lines",
            stackgroup="one",
            fillcolor=color.replace("#", "rgba(") + ",0.7)",
            line=dict(color=color, width=1.5),
            name=name,
            hovertemplate=f"<b>%{{x}}</b><br>{name}: $%{{y:,.0f}}<extra></extra>",
        ))
    fig.update_layout(xaxis_title="Month", yaxis_title="Revenue ($)")
    return _apply_layout(fig, "Monthly Revenue by Stream")


def fig_monthly_satisfaction(df: pd.DataFrame) -> go.Figure:
    """Line chart: avg satisfaction trend by month."""
    mdf = _monthly_df(df)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=mdf["Month_Label"],
        y=mdf["Avg_Satisfaction"],
        mode="lines+markers",
        line=dict(color="#FFB800", width=2.5),
        marker=dict(size=7, color="#FFB800"),
        hovertemplate="<b>%{x}</b><br>Avg Satisfaction: %{y:.2f}<extra></extra>",
        name="Avg Satisfaction",
    ))
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Avg Satisfaction Score",
        yaxis=dict(range=[0, 10]),
    )
    return _apply_layout(fig, "Monthly Avg Satisfaction Trend")


def fig_visit_heatmap(df: pd.DataFrame) -> go.Figure:
    """Heatmap: number of visits by Day of Week vs Month."""
    df2 = df.copy()
    df2["Day_of_Week"] = df2["Visit_Date"].dt.day_name()
    df2["Month_Label_Short"] = df2["Visit_Date"].dt.strftime("%b %Y")

    pivot = (
        df2.groupby(["Day_of_Week", "Month_Label"])["Customer_ID"]
        .count()
        .reset_index()
        .pivot(index="Day_of_Week", columns="Month_Label", values="Customer_ID")
        .fillna(0)
    )
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    pivot = pivot.reindex([d for d in day_order if d in pivot.index])

    # Sort columns chronologically
    months = df2.groupby("Month_Label")["Visit_Date"].min().sort_values().index.tolist()
    pivot = pivot.reindex(columns=[m for m in months if m in pivot.columns])

    fig = go.Figure(go.Heatmap(
        z=pivot.values,
        x=pivot.columns.tolist(),
        y=pivot.index.tolist(),
        colorscale=[[0, "#1A1F2E"], [0.5, "#7B68EE"], [1, "#FFD700"]],
        hovertemplate="<b>%{y}</b> – <b>%{x}</b><br>Visits: %{z}<extra></extra>",
    ))
    fig.update_layout(xaxis_title="Month", yaxis_title="Day of Week")
    return _apply_layout(fig, "Visit Heatmap: Day of Week × Month")


def fig_monthly_repeat_rate(df: pd.DataFrame) -> go.Figure:
    """Bar chart: repeat visit rate by month."""
    mdf = _monthly_df(df)
    fig = go.Figure(go.Bar(
        x=mdf["Month_Label"],
        y=mdf["Repeat_Rate"],
        marker_color="#4A9EFF",
        hovertemplate="<b>%{x}</b><br>Repeat Rate: %{y:.1f}%<extra></extra>",
    ))
    fig.update_layout(xaxis_title="Month", yaxis_title="Repeat Visit Rate (%)")
    return _apply_layout(fig, "Monthly Repeat Visit Rate")


def fig_monthly_customers_by_region(df: pd.DataFrame) -> go.Figure:
    """Grouped bar: customer count by month and seating region."""
    grp = (
        df.groupby(["Month_Label", "Seating_Region"])["Customer_ID"]
        .count()
        .reset_index()
    )
    grp.columns = ["Month_Label", "Seating_Region", "Customers"]

    # Sort months chronologically
    month_order = (
        df.groupby("Month_Label")["Visit_Date"].min()
        .sort_values()
        .index.tolist()
    )
    present_regions = [s for s in SEATING_ORDER if s in grp["Seating_Region"].unique()]

    fig = px.bar(
        grp,
        x="Month_Label",
        y="Customers",
        color="Seating_Region",
        barmode="group",
        color_discrete_map=SEATING_COLORS,
        category_orders={"Month_Label": month_order, "Seating_Region": present_regions},
        labels={"Customers": "Customer Count"},
    )
    fig.update_traces(hovertemplate="<b>%{x}</b><br>%{data.name}: %{y}<extra></extra>")
    return _apply_layout(fig, "Monthly Customers by Seating Region")
