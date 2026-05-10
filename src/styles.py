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
    plot_bgcolor="rgba(8,13,26,0.7)",
    font=dict(family="'Inter', sans-serif", color="#FAFAFA", size=12),
    margin=dict(l=40, r=20, t=50, b=40),
    legend=dict(
        bgcolor="rgba(17,24,39,0.85)",
        bordercolor="rgba(255,255,255,0.06)",
        borderwidth=1,
        font=dict(family="'Inter', sans-serif", size=11),
    ),
    xaxis=dict(
        gridcolor="rgba(255,255,255,0.04)",
        linecolor="rgba(255,255,255,0.12)",
        tickfont=dict(family="'Inter', sans-serif", size=11),
        title_font=dict(family="'Inter', sans-serif", size=12),
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.04)",
        linecolor="rgba(255,255,255,0.12)",
        tickfont=dict(family="'Inter', sans-serif", size=11),
        title_font=dict(family="'Inter', sans-serif", size=12),
    ),
)


# ── CSS Injection ───────────────────────────────────────────────────────────

def inject_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        html, body, [class*="css"], .stApp, .stMarkdown, button, input, select, textarea, label {
            font-family: 'Inter', sans-serif !important;
        }

        #MainMenu { visibility: hidden; }
        footer    { visibility: hidden; }
        header    { visibility: hidden; }

        ::-webkit-scrollbar             { width: 5px; height: 5px; }
        ::-webkit-scrollbar-track       { background: transparent; }
        ::-webkit-scrollbar-thumb       { background: rgba(255,255,255,0.12); border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: rgba(255,107,107,0.45); }

        .stApp {
            background:
                radial-gradient(ellipse at 20% 10%, rgba(255,107,107,0.04) 0%, transparent 60%),
                radial-gradient(ellipse at 80% 90%, rgba(74,158,255,0.03) 0%, transparent 55%),
                #080D1A;
            background-attachment: fixed;
        }

        .main .stMarkdown h2 {
            font-size: 32px !important;
            font-weight: 700 !important;
            color: #FAFAFA !important;
            margin-top: 40px !important;
            margin-bottom: 20px !important;
        }

        .main .stMarkdown h3 {
            font-size: 26px !important;
            font-weight: 600 !important;
            color: #FAFAFA !important;
            margin-top: 30px !important;
            margin-bottom: 15px !important;
        }

        section[data-testid="stSidebar"],
        section[data-testid="stSidebar"] *,
        [data-testid="stSidebarNav"],
        [data-testid="stSidebarNav"] * {
            transition: none !important;
            animation: none !important;
        }

        section[data-testid="stSidebar"] {
            transform: translateX(0) !important;
            min-width: 21rem !important;
            visibility: visible !important;
            background: linear-gradient(180deg, #0D1425 0%, #0A1020 60%, #080D1A 100%);
            border-right: 1px solid rgba(255,255,255,0.06);
        }
        [data-testid="collapsedControl"],
        [data-testid="stSidebarCollapseButton"] { display: none !important; }

        /* Sidebar Navigation Styling */
        [data-testid="stSidebarNav"] {
            padding-top: 1rem !important;
        }
        [data-testid="stSidebarNav"] ul {
            padding-top: 0 !important;
        }
        [data-testid="stSidebarNav"] span {
            font-size: 18px !important;
            font-weight: 500 !important;
            color: rgba(255,255,255,0.85) !important;
        }
        [data-testid="stSidebarNav"] a {
            padding: 10px 16px !important;
            border-radius: 10px !important;
            margin: 4px 12px !important;
        }
        [data-testid="stSidebarNav"] a:hover {
            background-color: rgba(255,255,255,0.05) !important;
        }
        [data-testid="stSidebarNav"] [data-testid="stSidebarNavActive"] {
            background-color: rgba(255,107,107,0.12) !important;
            border: 1px solid rgba(255,107,107,0.2) !important;
        }
        [data-testid="stSidebarNav"] [data-testid="stSidebarNavActive"] span {
            color: #FF6B6B !important;
            font-weight: 600 !important;
        }

        section[data-testid="stSidebar"] .stMarkdown h2 {
            font-size: 24px !important;
            font-weight: 700 !important;
            letter-spacing: 0.04em !important;
            text-transform: uppercase !important;
            color: rgba(255,255,255,0.7) !important;
            margin-bottom: 15px !important;
        }
        section[data-testid="stSidebar"] label {
            font-size: 16px !important;
            font-weight: 600 !important;
            letter-spacing: 0.02em !important;
            text-transform: uppercase !important;
            color: rgba(255,255,255,0.6) !important;
        }
        section[data-testid="stSidebar"] [data-baseweb="select"] > div,
        section[data-testid="stSidebar"] [data-baseweb="input"] > div {
            background: rgba(255,255,255,0.04) !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
            border-radius: 8px !important;
            min-height: 45px !important;
        }
        section[data-testid="stSidebar"] [data-baseweb="select"] > div:hover {
            border-color: rgba(255,107,107,0.4) !important;
        }
        section[data-testid="stSidebar"] .stButton > button {
            background: rgba(255,107,107,0.08) !important;
            border: 1px solid rgba(255,107,107,0.25) !important;
            color: #FF6B6B !important;
            border-radius: 8px !important;
            font-size: 12px !important;
            font-weight: 500 !important;
            letter-spacing: 0.03em !important;
        }
        section[data-testid="stSidebar"] .stButton > button:hover {
            background: rgba(255,107,107,0.16) !important;
            border-color: rgba(255,107,107,0.5) !important;
        }

        .kpi-card {
            background: linear-gradient(135deg, rgba(255,255,255,0.055) 0%, rgba(255,255,255,0.020) 100%);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-radius: 16px;
            padding: 24px 28px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.45), 0 1px 0 rgba(255,255,255,0.07) inset;
            margin-bottom: 8px;
            border: 1px solid rgba(255,255,255,0.07);
            border-left: 4px solid;
            height: 140px;
            position: relative;
            overflow: hidden;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .kpi-card::before {
            content: '';
            position: absolute;
            top: 0; left: 4px; right: 0;
            height: 1px;
            background: linear-gradient(90deg, rgba(255,255,255,0.18) 0%, transparent 70%);
        }
        .kpi-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 40px rgba(0,0,0,0.55), 0 1px 0 rgba(255,255,255,0.09) inset;
        }
        .kpi-value {
            font-size: 36px !important;
            font-weight: 600 !important;
            color: #FAFAFA;
            margin: 0;
            line-height: 1.2;
            letter-spacing: -0.02em;
        }
        .kpi-label {
            font-size: 18px;
            color: rgba(156,163,175,0.9);
            margin: 8px 0 0 0;
            text-transform: uppercase;
            letter-spacing: 0.07em;
            font-weight: 600;
        }
        .kpi-delta {
            font-size: 14px;
            font-weight: 500;
            margin-top: 8px;
            letter-spacing: 0.01em;
        }
        .delta-positive { color: #00C48C; }
        .delta-negative { color: #FF6B6B; }
        .delta-neutral  { color: rgba(156,163,175,0.8); }

        .section-header {
            font-size: 28px;
            font-weight: 700;
            color: #FAFAFA;
            letter-spacing: 0.01em;
            margin: 32px 0 16px 0;
            padding-left: 16px;
            position: relative;
        }
        .section-header::before {
            content: '';
            position: absolute;
            left: 0;
            top: 50%;
            transform: translateY(-50%);
            width: 4px;
            height: 100%;
            background: linear-gradient(180deg, #FF6B6B 0%, rgba(255,107,107,0.3) 100%);
            border-radius: 2px;
        }

        .page-title {
            font-size: 48px;
            font-weight: 800;
            color: #FAFAFA;
            margin-bottom: 8px;
            letter-spacing: -0.03em;
            line-height: 1.1;
        }
        .page-title-accent {
            display: block;
            width: 64px;
            height: 4px;
            background: linear-gradient(90deg, #FF6B6B 0%, rgba(255,107,107,0) 100%);
            border-radius: 2px;
            margin-bottom: 12px;
        }
        .page-subtitle {
            font-size: 22px;
            color: rgba(156,163,175,0.9);
            margin-bottom: 32px;
            font-weight: 400;
            letter-spacing: 0.01em;
        }

        .main hr, [data-testid="stVerticalBlock"] hr, hr.styled {
            border: none !important;
            height: 1px !important;
            background: linear-gradient(90deg, rgba(255,107,107,0.35) 0%, rgba(255,255,255,0.06) 30%, transparent 100%) !important;
            margin: 24px 0 !important;
        }

        [data-testid="stMetric"] {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 12px;
            padding: 14px 16px !important;
        }
        [data-testid="stMetricLabel"] {
            font-size: 16px !important;
            font-weight: 600 !important;
            letter-spacing: 0.06em !important;
            text-transform: uppercase !important;
            color: rgba(156,163,175,0.8) !important;
        }
        [data-testid="stMetricValue"] {
            font-size: 28px !important;
            font-weight: 700 !important;
            letter-spacing: -0.01em !important;
        }

        [data-testid="stExpander"] {
            border: 1px solid rgba(255,255,255,0.07) !important;
            border-radius: 12px !important;
            background: rgba(255,255,255,0.025) !important;
            overflow: hidden;
        }
        [data-testid="stExpander"] summary {
            font-size: 18px !important;
            font-weight: 600 !important;
            padding: 12px 16px !important;
        }
        [data-testid="stExpander"] summary:hover {
            background: rgba(255,255,255,0.03) !important;
        }

        [data-testid="stAlert"] {
            background: rgba(74,158,255,0.08) !important;
            border: 1px solid rgba(74,158,255,0.2) !important;
            border-radius: 10px !important;
            font-size: 13px !important;
        }

        [data-testid="stDataFrame"] > div {
            border: 1px solid rgba(255,255,255,0.07) !important;
            border-radius: 10px !important;
            overflow: hidden;
        }

        [data-baseweb="select"] > div {
            background: rgba(255,255,255,0.04) !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            border-radius: 8px !important;
            font-size: 13px !important;
        }
        [data-baseweb="select"] > div:focus-within {
            border-color: rgba(255,107,107,0.5) !important;
            box-shadow: 0 0 0 2px rgba(255,107,107,0.12) !important;
        }

        [data-testid="stPlotlyChart"] {
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.05);
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
    st.markdown(
        f'<div class="page-title">{title}</div>'
        f'<div class="page-title-accent"></div>',
        unsafe_allow_html=True,
    )
    if subtitle:
        st.markdown(f'<div class="page-subtitle">{subtitle}</div>', unsafe_allow_html=True)
