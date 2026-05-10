import pandas as pd


def TotalTicketRevenue(df: pd.DataFrame) -> float:
    return df["Ticket_Revenue"].sum()


def TotalMerchandiseRevenue(df: pd.DataFrame) -> float:
    return df["Merchandise_Spend"].sum()


def TotalDrinkRevenue(df: pd.DataFrame) -> float:
    return df["Drink_Spend"].sum()


def TotalRevenue(df: pd.DataFrame) -> float:
    return df["Total_Spend"].sum()


def AverageSpendPerCustomer(df: pd.DataFrame) -> float:
    return df["Total_Spend"].mean()


def RepeatVisitRate(df: pd.DataFrame) -> float:
    if len(df) == 0:
        return 0.0
    return (df["Repeat_Visit"] == 1).sum() / len(df) * 100


def AverageSatisfaction(df: pd.DataFrame) -> float:
    return df["Satisfaction_Score"].mean()


def AverageRecommendation(df: pd.DataFrame) -> float:
    return df["Recommendation_Likelihood"].mean()


def HighlySatisfiedPct(df: pd.DataFrame, threshold: float = 7.0) -> float:
    if len(df) == 0:
        return 0.0
    return (df["Satisfaction_Score"] >= threshold).sum() / len(df) * 100


def fmt_currency(value: float) -> str:
    if value >= 1_000_000:
        return f"${value/1_000_000:.2f}M"
    elif value >= 1_000:
        return f"${value/1_000:.1f}K"
    return f"${value:.2f}"


def fmt_pct(value: float) -> str:
    return f"{value:.1f}%"


def fmt_score(value: float) -> str:
    return f"{value:.2f}"


def fmt_count(value: int) -> str:
    return f"{value:,}"
