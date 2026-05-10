# RUN & PUBLISH INSTRUCTIONS

## DataXplore 2.0 — Company X Analytics Dashboard

---

## Prerequisites

- Python **3.9+** installed
- `pip` available in your terminal
- Git installed (for deployment)

---

## 1. Local Development

### Step 1 — Clone / Navigate to the project

```bash
cd "Bayesian_Minds-DataXplore_2-0_Stage_03"
```

### Step 2 — Create a virtual environment (recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Run the dashboard

```bash
streamlit run app.py
```

The dashboard will open automatically at **http://localhost:8501**

### Pages

| URL | Page |
|---|---|
| `http://localhost:8501` | Overview |
| `http://localhost:8501/Revenue_Analysis` | Revenue Analysis |
| `http://localhost:8501/Customer_Analysis` | Customer Analysis |
| `http://localhost:8501/Experience_Analysis` | Experience Analysis |
| `http://localhost:8501/Time_Based_Analysis` | Time-Based Analysis |

---

## 2. Deploy to Streamlit Community Cloud (Free)

### Step 1 — Push to GitHub

```bash
git add .
git commit -m "Add DataXplore 2.0 dashboard"
git push origin main
```

Make sure your repository is **public** (or you have Streamlit Cloud connected to a private repo).

### Step 2 — Deploy

1. Go to **https://share.streamlit.io**
2. Sign in with GitHub
3. Click **"New app"**
4. Select your repository, branch (`main`), and main file (`app.py`)
5. Click **"Deploy"**

Your app will be live at:
```
https://<github-username>-<repo-name>-app-<hash>.streamlit.app
```

### Step 3 — Configure secrets / settings (optional)

Streamlit Cloud uses `.streamlit/config.toml` from your repo automatically — the dark theme will apply.

---

## 3. Deploy to Render.com (Alternative Free Hosting)

### Step 1 — Create `Procfile` in project root

```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

### Step 2 — Push to GitHub (if not already done)

```bash
git add .
git commit -m "Add Render deployment config"
git push origin main
```

### Step 3 — Create Render Web Service

1. Go to **https://render.com** and sign up / log in
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Set the following:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
   - **Environment:** Python 3
   - **Plan:** Free
5. Click **"Create Web Service"**

Your app will be live at:
```
https://<service-name>.onrender.com
```

> **Note:** Free Render services spin down after inactivity — first load may take 30–60 seconds.

---

## 4. Project Structure Reference

```
project_root/
├── app.py                          # Main entry point (Overview page)
├── requirements.txt                # Python dependencies
├── RUN.md                          # This file
├── PLAN.md                         # Implementation plan
├── .streamlit/
│   └── config.toml                 # Dark theme configuration
├── data/
│   └── Company_X_Audience.csv      # Dataset (800 rows)
├── src/
│   ├── __init__.py
│   ├── data_loader.py              # CSV loading with caching
│   ├── data_prep.py                # Type casting + derived columns
│   ├── star_schema.py              # Fact & dimension tables
│   ├── kpi.py                      # KPI calculation functions
│   ├── charts.py                   # Plotly figure factories
│   ├── filters.py                  # Sidebar filter widgets
│   └── styles.py                   # CSS, KPI cards, color palettes
└── pages/
    ├── 1_Revenue_Analysis.py
    ├── 2_Customer_Analysis.py
    ├── 3_Experience_Analysis.py
    └── 4_Time_Based_Analysis.py
```

---

## 5. Troubleshooting

| Issue | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'streamlit'` | Run `pip install -r requirements.txt` |
| `FileNotFoundError: data/Company_X_Audience.csv` | Ensure `data/` folder exists with the CSV |
| Charts not rendering | Ensure `plotly>=5.18.0` is installed |
| OLS trendlines not working | Run `pip install statsmodels` |
| Slow first load | Data is cached after first run — subsequent page switches are fast |
| Port already in use | Run `streamlit run app.py --server.port 8502` |
