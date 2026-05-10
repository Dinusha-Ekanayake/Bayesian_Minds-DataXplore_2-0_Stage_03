import streamlit as st

# ── Color Palettes ──────────────────────────────────────────────────────────

SEATING_COLORS = {
    "VIP": "#FFD700",
    "Premium": "#7B68EE",
    "High Economy": "#00CED1",
    "Economy": "#FF6B6B",
}

GENDER_COLORS = {
    "Male": "#4A9EFF",
    "Female": "#FF6B9D",
    "Other": "#50E3C2",
}

REVENUE_STREAM_COLORS = {
    "Ticket Revenue": "#FF6B6B",
    "Merchandise Spend": "#4ECDC4",
    "Drink Spend": "#FFE66D",
}

COUNTRY_COLORS = {
    "Australia": "#FF6B6B",
    "France": "#4A9EFF",
    "Germany": "#FFE66D",
    "Japan": "#50E3C2",
    "Sweden": "#FF6B9D",
    "UK": "#7B68EE",
    "USA": "#FFD700",
}

AGE_GROUP_COLORS = {
    "18-25": "#FF6B6B",
    "26-35": "#4ECDC4",
    "36-45": "#FFE66D",
    "46-55": "#7B68EE",
    "56-65": "#FF6B9D",
    "66+": "#50E3C2",
}

SPEND_TIER_COLORS = {
    "Low": "#50E3C2",
    "Medium": "#FFE66D",
    "High": "#FF6B9D",
    "Premium": "#FFD700",
}

KPI_ACCENT = {
    "revenue": "#00C48C",
    "customer": "#4A9EFF",
    "experience": "#FFB800",
    "time": "#A78BFA",
}

PLOTLY_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(14,17,23,0.6)",
    font=dict(family="sans-serif", color="#FAFAFA"),
    margin=dict(l=40, r=20, t=50, b=40),
    legend=dict(
        bgcolor="rgba(26,31,46,0.8)",
        bordercolor="rgba(255,255,255,0.1)",
        borderwidth=1,
    ),
)


# ── CSS Injection ───────────────────────────────────────────────────────────

def inject_css():
    st.markdown(
        """
        <style>
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Main background */
        .stApp {
            background-color: #0E1117;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #1A1F2E;
            border-right: 1px solid rgba(255,255,255,0.08);
        }

        /* KPI Card */
        .kpi-card {
            background: #1A1F2E;
            border-radius: 12px;
            padding: 18px 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            margin-bottom: 8px;
            border-left: 4px solid;
            height: 110px;
        }
        .kpi-value {
            font-size: 28px;
            font-weight: 700;
            color: #FAFAFA;
            margin: 0;
            line-height: 1.2;
        }
        .kpi-label {
            font-size: 12px;
            color: #9CA3AF;
            margin: 4px 0 0 0;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .kpi-delta {
            font-size: 13px;
            margin-top: 6px;
        }
        .delta-positive { color: #00C48C; }
        .delta-negative { color: #FF6B6B; }
        .delta-neutral  { color: #9CA3AF; }

        /* Section headers */
        .section-header {
            font-size: 18px;
            font-weight: 600;
            color: #FAFAFA;
            border-bottom: 2px solid #FF6B6B;
            padding-bottom: 6px;
            margin: 24px 0 16px 0;
        }

        /* Page title */
        .page-title {
            font-size: 32px;
            font-weight: 700;
            color: #FAFAFA;
            margin-bottom: 4px;
        }
        .page-subtitle {
            font-size: 14px;
            color: #9CA3AF;
            margin-bottom: 24px;
        }

        /* Divider */
        hr.styled {
            border: none;
            border-top: 1px solid rgba(255,255,255,0.08);
            margin: 20px 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ── KPI Card HTML ───────────────────────────────────────────────────────────

def kpi_card(label: str, value: str, delta: str = "", category: str = "revenue") -> str:
    accent = KPI_ACCENT.get(category, "#FF6B6B")
    if delta:
        if delta.startswith("+") or (delta.replace(".", "").replace("%", "").replace("+", "").lstrip("-").isdigit() and not delta.startswith("-")):
            delta_class = "delta-positive"
        elif delta.startswith("-"):
            delta_class = "delta-negative"
        else:
            delta_class = "delta-neutral"
        delta_html = f'<p class="kpi-delta {delta_class}">{delta}</p>'
    else:
        delta_html = ""

    return f"""
    <div class="kpi-card" style="border-left-color: {accent};">
        <p class="kpi-value">{value}</p>
        <p class="kpi-label">{label}</p>
        {delta_html}
    </div>
    """


def render_kpi_row(cards: list):
    """Render a row of KPI cards. Each card is a dict with label, value, delta, category."""
    cols = st.columns(len(cards))
    for col, card in zip(cols, cards):
        with col:
            st.markdown(
                kpi_card(
                    card["label"],
                    card["value"],
                    card.get("delta", ""),
                    card.get("category", "revenue"),
                ),
                unsafe_allow_html=True,
            )


def section_header(title: str):
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)


def page_header(title: str, subtitle: str = ""):
    st.markdown(f'<div class="page-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="page-subtitle">{subtitle}</div>', unsafe_allow_html=True)
