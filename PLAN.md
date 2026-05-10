# Streamlit Customer Analytics Dashboard - Implementation Plan

## Context

Building a Python Streamlit dashboard for a live entertainment venue's customer analytics hackathon. Dataset: `Company_X_Audience.csv` (800 rows, 13 columns, no nulls). The dashboard covers **Revenue**, **Customer**, **Experience**, and **Time-Based** analysis with star schema modeling, interactive filters, and a modern dark-themed UI.

---

## Folder Structure

```
project_root/
|-- app.py                        # Landing/overview page (main entry point)
|-- requirements.txt              # Python dependencies
|-- .streamlit/
|   |-- config.toml               # Dark theme configuration
|-- data/
|   |-- Company_X_Audience.csv    # Raw dataset
|-- src/
|   |-- data_loader.py            # Load CSV with @st.cache_data
|   |-- data_prep.py              # Cleaning, type casting, derived columns
|   |-- star_schema.py            # Fact + dimension table construction
|   |-- kpi.py                    # KPI computation functions
|   |-- charts.py                 # Plotly figure factory functions
|   |-- filters.py                # Reusable sidebar filter widgets
|   |-- styles.py                 # CSS injection, metric card HTML, color maps
|-- pages/
|   |-- 1_Revenue_Analysis.py     # Revenue breakdown & comparisons
|   |-- 2_Customer_Analysis.py    # Demographics, spending, repeat visits
|   |-- 3_Experience_Analysis.py  # Satisfaction & recommendation analysis
|   |-- 4_Time_Based_Analysis.py  # Monthly trends & temporal patterns
```

---

## Tech Stack

| Library | Purpose |
|---|---|
| `streamlit` >= 1.32 | Dashboard framework, multi-page app |
| `pandas` >= 2.0 | Data manipulation & transformations |
| `plotly` >= 5.18 | All interactive charts |
| `numpy` >= 1.24 | Numerical operations |

---

## Implementation Stages

### Stage 1: Project Setup

- Create folder structure: `data/`, `src/`, `pages/`, `.streamlit/`
- Move CSV to `data/Company_X_Audience.csv`
- Create `requirements.txt`
- Configure `.streamlit/config.toml` with dark theme:
  - Background: `#0E1117`, Secondary: `#1A1F2E`, Accent: `#FF6B6B`, Text: `#FAFAFA`

---

### Stage 2: Data Preparation (`src/data_loader.py` + `src/data_prep.py`)

**Type casting:**
- `Visit_Date` -> datetime
- Ensure all numeric columns are proper types

**Derived columns:**
| Column | Formula |
|---|---|
| `Ticket_Revenue` | `Ticket_Price * Num_Tickets` |
| `Total_Spend` | `Ticket_Revenue + Merchandise_Spend + Drink_Spend` |
| `Month_Label` | e.g., "Jan 2025" |
| `Visit_Quarter` | e.g., "Q1 2025" |
| `Age_Group` | 18-25, 26-35, 36-45, 46-55, 56-65, 66+ |
| `Visit_Type` | "Repeat" / "First-time" (from Repeat_Visit) |
| `Spend_Tier` | Low / Medium / High / Premium (quartile-based) |

All data loading cached with `@st.cache_data` for performance.

---

### Stage 3: Star Schema Data Model (`src/star_schema.py`)

```
              dim_customer
                   |
dim_date --- fact_transactions --- dim_seating
                   |
              dim_geography
```

| Table | Key Columns |
|---|---|
| **fact_transactions** | Customer_ID (FK), Date_Key (FK), Seating_Key (FK), Country_Key (FK), Ticket_Revenue, Merchandise_Spend, Drink_Spend, Total_Spend, Num_Tickets, Repeat_Visit, Satisfaction_Score, Recommendation_Likelihood |
| **dim_customer** | Customer_ID (PK), Age, Gender, Age_Group, Spend_Tier |
| **dim_date** | Date_Key (PK), Visit_Date, Day, Month, Month_Name, Quarter, Year, Day_of_Week, Week_Number |
| **dim_seating** | Seating_Key (PK), Seating_Region, Ticket_Price |
| **dim_geography** | Country_Key (PK), Country, Continent |

---

### Stage 4: Styling & Theming (`src/styles.py`)

**Custom KPI metric cards** using HTML/CSS:
- Dark card background (`#1A1F2E`), rounded corners, subtle shadow
- Left-border accent color by category:
  - Revenue = green, Customer = blue, Experience = amber, Time = purple
- Large number display + small label + delta indicator

**Consistent color palettes:**
| Category | Colors |
|---|---|
| Seating Regions | VIP: `#FFD700`, Premium: `#7B68EE`, High Economy: `#00CED1`, Economy: `#FF6B6B` |
| Gender | Male: `#4A9EFF`, Female: `#FF6B9D`, Other: `#50E3C2` |
| Revenue Streams | Ticket: `#FF6B6B`, Merchandise: `#4ECDC4`, Drink: `#FFE66D` |

**Plotly defaults:** Dark template, transparent backgrounds, consistent font sizes.

---

### Stage 5: Interactive Filters (`src/filters.py`)

Sidebar filters (persistent across pages via `st.session_state`):
- Date range slider (Jan 2025 - Sep 2025)
- Country multi-select (7 countries)
- Seating Region multi-select (4 regions)
- Gender multi-select (Male / Female / Other)
- Age Group multi-select (6 groups)
- Visit Type toggle (All / First-time / Repeat)

---

### Stage 6: KPI Functions (`src/kpi.py`)

| KPI | Description |
|---|---|
| `TotalTicketRevenue` | Sum of Ticket_Revenue |
| `TotalMerchandiseRevenue` | Sum of Merchandise_Spend |
| `TotalDrinkRevenue` | Sum of Drink_Spend |
| `TotalRevenue` | Sum of Total_Spend |
| `AverageSpendPerCustomer` | Mean of Total_Spend |
| `RepeatVisitRate` | % of Repeat_Visit == 1 |
| `AverageSatisfaction` | Mean of Satisfaction_Score |
| `AverageRecommendation` | Mean of Recommendation_Likelihood |

---

### Stage 7: Dashboard Pages

#### Overview Page (`app.py`)
- **4 KPI cards**: Total Revenue, Total Customers, Repeat Visit Rate, Avg Satisfaction
- Star schema diagram visualization
- Project description & navigation guide

#### Page 1: Revenue Analysis
| Visual | Type | Purpose |
|---|---|---|
| KPI row | 4 metric cards | Ticket/Merch/Drink Revenue + Avg Spend |
| Revenue by Seating Region | Stacked bar | Which regions generate most value |
| Revenue by Country | Grouped bar | Geographic revenue comparison |
| Revenue by Country > Region | Treemap | Proportional contribution |
| Revenue by Age Group | Horizontal bar | Customer group contribution (colored by Visit Type) |
| Revenue hierarchy | Sunburst | Country > Seating > Gender drill-down |

#### Page 2: Customer Analysis
| Visual | Type | Purpose |
|---|---|---|
| KPI row | 4 metric cards | Customers, Avg Tickets, Repeat Rate, Avg Spend |
| Gender distribution | Donut chart | Demographic split |
| Seating distribution | Donut chart | Seating preferences |
| Age distribution | Histogram | Age profile by gender |
| Geographic distribution | Choropleth map | Customer count by country |
| Spend by Region | Box plot | Spending distribution & outliers |
| Repeat vs First-time spend | Grouped bar | Do repeat visitors spend more? |
| Age vs Spend | Scatter plot | Relationship (colored by region, sized by tickets) |

#### Page 3: Experience Analysis
| Visual | Type | Purpose |
|---|---|---|
| KPI row | 4 metric cards | Avg Satisfaction, Avg Recommendation, Highly Satisfied % |
| Satisfaction by Region & Visit Type | Grouped bar | Segment comparison |
| Recommendation by Country | Grouped bar | Geographic comparison |
| Spend vs Satisfaction | Scatter + trendline | Correlation analysis |
| Spend vs Recommendation | Scatter + trendline | Correlation analysis |
| Correlation matrix | Heatmap | Multi-variable relationships |
| Satisfaction distribution | Violin plot | Distribution by seating region |
| Country comparison | Radar chart | Satisfaction & recommendation overlay |

#### Page 4: Time-Based Analysis
| Visual | Type | Purpose |
|---|---|---|
| KPI row | 4 metric cards | Best/Worst Month, MoM Growth, Peak Day |
| Monthly revenue trend | Line chart (area fill) | Revenue over time |
| Monthly revenue by stream | Stacked area | Ticket/Merch/Drink trends |
| Monthly satisfaction trend | Line chart | Experience over time |
| Visit heatmap | Heatmap | Day of Week vs Month patterns |
| Monthly repeat rate | Bar chart | Repeat visit trends |
| Monthly customers by region | Grouped bar | Seating mix over time |

---

### Stage 8: Deployment

1. Push to GitHub repository
2. Deploy on **Streamlit Community Cloud** (share.streamlit.io)
3. Get public URL: `https://<user>-<repo>.streamlit.app`
4. Alternative: Render.com free tier

---

## Verification Checklist

- [ ] `streamlit run app.py` - all 5 pages load without errors
- [ ] All sidebar filters work and persist across page navigation
- [ ] KPI values match manual calculations from CSV
- [ ] Charts are interactive (hover, zoom, click)
- [ ] Dark theme renders consistently across all pages
- [ ] Responsive layout works at different browser widths
- [ ] Deployed URL is publicly accessible
- [ ] Star schema model is documented and visualized

---

## Dataset Summary

- **Rows**: 800 (no nulls, no duplicates on Customer_ID)
- **Date range**: Jan 1, 2025 - Sep 8, 2025
- **Countries**: Australia, France, Germany, Japan, Sweden, UK, USA
- **Seating**: VIP ($200), Premium ($150), High Economy ($100), Economy ($60)
- **Gender**: Male, Female, Other
- **Age range**: 18-69
