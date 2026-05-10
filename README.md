# DataXplore 2.0 - Company X Analytics Dashboard

Developed by **Team Bayesian Minds** for the DataXplore 2.0 Hackathon.

---

## 🚀 Project Overview
**DataXplore 2.0** is an interactive business intelligence solution designed for a live entertainment venue (Company X). The dashboard transforms raw customer-level data into actionable insights, helping management understand revenue performance, customer behavior, and experience quality.

The project analyzes 800 customer records spanning from January to September 2025 across 7 countries and 4 seating tiers.

### Key Business Questions Addressed:
*   Which customer segments contribute most to total revenue?
*   How do satisfaction and recommendation scores vary across demographics?
*   What are the monthly and daily trends in venue traffic and spending?
*   Do repeat visitors exhibit different spending patterns than first-time guests?

---

## 📊 Dashboard Sections
The dashboard is built with **Streamlit** and features five specialized analysis pages:

| Page | Description |
|---|---|
| **🏠 Overview** | High-level KPIs (Total Revenue, Customers, Repeat Rate, Satisfaction) and dataset summary. |
| **💰 Revenue Analysis** | Breakdown of Ticket, Merchandise, and Drink revenue by region, country, and age. |
| **👥 Customer Analysis** | Demographic (Age/Gender) and geographic distribution of the audience. |
| **⭐ Experience Analysis** | Correlation between spending and satisfaction; NPS-style recommendation metrics. |
| **📅 Time-Based Analysis** | Monthly trends and seasonal patterns (with partial September data excluded for accuracy). |

---

## 🛠️ Tech Stack & Architecture
*   **Frontend/App:** [Streamlit](https://streamlit.io/)
*   **Visualizations:** [Plotly](https://plotly.com/python/)
*   **Data Processing:** Pandas, NumPy
*   **Data Modeling:** Implemented using a **Star Schema** (Fact transactions with dimensions for Customer, Date, Geography, and Seating) to ensure efficient analytical querying.

---

## ⚙️ Run & Publish Instructions

### Prerequisites
- Python **3.9+** installed
- `pip` available in your terminal
- Git installed (for deployment)

### 1. Local Development

**Step 1 — Clone / Navigate to the project**
```bash
cd "Bayesian_Minds-DataXplore_2-0_Stage_03"
```

**Step 2 — Create a virtual environment (recommended)**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

**Step 3 — Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 4 — Run the dashboard**
```bash
streamlit run Home.py
```
The dashboard will open automatically at **http://localhost:8501**

---

### 2. Deploy to Streamlit Community Cloud (Free)

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Final dashboard submission"
   git push origin main
   ```
2. **Deploy:**
   - Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
   - Click **"New app"** and select your repository, branch (`main`), and main file (`Home.py`).
   - Click **"Deploy"**.

---

### 3. Deploy to Render.com (Alternative)

1. Ensure a `Procfile` exists with: `web: streamlit run Home.py --server.port=$PORT --server.address=0.0.0.0`
2. Create a new **Web Service** on Render, connect your GitHub repo, and use:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run Home.py --server.port=$PORT --server.address=0.0.0.0`

---

## 📁 Project Structure
```
.
├── Home.py                 # Main entry point (Overview page)
├── requirements.txt        # Python dependencies
├── .streamlit/             # Theme & UI config
├── data/                   # Raw dataset (CSV)
├── pages/                  # Multipage dashboard scripts
└── src/                    # Modular logic (loader, prep, schema, charts, styles)
```

---

## 🛠️ Troubleshooting

| Issue | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'streamlit'` | Run `pip install -r requirements.txt` |
| `FileNotFoundError: data/...` | Ensure the `data/` folder contains the necessary CSV files. |
| Charts not rendering | Ensure `plotly>=5.18.0` is installed. |
| Slow first load | Data is cached after the first run — subsequent navigation is fast. |

---

## 👥 Team Bayesian Minds
*   **Dinusha Ekanayake**
*   **Kavinda Mihiran**
*   **Amandi Arangala**
*   **Tharusha Udana**

---
*Created for the DataXplore 2.0 Dashboard Hackathon - April 2026.*
