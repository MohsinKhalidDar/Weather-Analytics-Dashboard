# 🌦️ Weather Analytics Dashboard (Industry-Grade)

An **analytics-first Weather Intelligence Dashboard** built with **Streamlit + Python**, designed like real monitoring tools used by **data analytics, risk, and operations teams**.

This project is not a basic API wrapper — it follows **production-style architecture**, includes **historical storage (SQLite)**, **trend analytics**, **5-day forecast**, **forecast accuracy tracking**, and **API observability (latency monitoring + status)**.

🔗 **Live Demo:** https://weatheranalyticsdashboard.streamlit.app/

---

## 🚀 Project Overview

Weather impacts decision-making across industries like:

✅ Logistics & delivery operations  
✅ Risk monitoring & disaster response  
✅ Travel, events & planning systems  
✅ Energy demand forecasting  
✅ Smart city infrastructure dashboards  

This dashboard provides:

- Real-time weather insights
- Analytics-style KPIs
- Historical trend tracking
- Forecast intelligence with conditions + rain probability
- Forecast accuracy tracking (Actual vs Predicted)

---

## ✨ Key Features

### ✅ Live Weather Intelligence (OpenWeather)
- City-based search (works globally)
- Temperature, Feels-like, Humidity, Pressure, Wind
- Condition summary + comfort/health scoring
- KPI cards for fast decision insights

### ✅ Historical Storage + Trend Analytics (SQLite)
- Stores every weather snapshot in a local SQLite database
- Temperature and health trends plotted from historical runs
- Helps build long-term monitoring insights

### ✅ Forecast Analytics (WeatherAPI)
- **Next 5-day forecast**
- Min / Max / Avg temperature forecast
- Weather conditions + icons
- Rain probability visualization

### ✅ Smart Weather Alerts
Auto alerts based on forecast thresholds:
- Heatwave risk ☀️
- Cold wave risk ❄️
- Heavy rain probability 🌧️

### ✅ Forecast Accuracy Tracking (Model Monitoring)
- Tracks **predicted vs actual**
- Computes error metrics (MAE)
- Shows **accuracy trend chart**
- Similar to monitoring real prediction pipelines used in fintech/ML systems

### ✅ Observability / Reliability
- API latency monitoring
- Safe error handling (timeouts / failures)
- Caching logic for forecast fallback

---

## 🛠 Tech Stack

- **Frontend / Dashboard:** Streamlit
- **Visualization:** Plotly
- **Data processing:** Pandas
- **APIs:**
  - OpenWeather API (current weather)
  - WeatherAPI (forecast + conditions)
- **Storage:** SQLite
- **Environment & Secrets:** `.env` (local), Streamlit Secrets (cloud deployment)

---

⚙️ Setup Instructions (Local)

✅ 1) Clone the repository
```
  git clone https://github.com/MohsinKhalidDar/Weather-Analytics-Dashboard.git

  cd Weather-Analytics-Dashboard
```
  
✅ 2) Create a virtual environment
```
  python -m venv venv (bash)
```
  
✅ 3) Install dependencies   
```
  pip install -r requirements.txt
````
  
✅ 4) Add API keys (Local .env)
```
  WEATHER_API_KEY=your_openweather_key
  WEATHERAPI_KEY=your_weatherapi_key

  BASE_URL=https://api.openweathermap.org/data/2.5

  WEATHERAPI_BASE_URL=https://api.weatherapi.com/v1
  REQUEST_TIMEOUT=10
```
  
✅ 5) Run the dashboard
```
  streamlit run app.py
```

--

📸 Screenshots
  Dashboard overview

  Historical trends

  Forecast + outlook cards

  Alerts section

--

✅ Usage Guide

1.Enter any city name in sidebar

2.Click Analyze Weather

3.View:
  KPI Insights.
  Historical trends (builds over multiple runs).
  5-day forecast.
  Weather alerts.
  Forecast accuracy tracking (builds over days).



🔮Future Improvements
  City-to-city comparison
  Auto-refresh scheduling
  DuckDB support for analytics scaling
  Advanced anomaly detection (temperature spikes, unusual humidity trends)
  Email/Slack alerting for severe weather events
  Deploy database to PostgreSQL (Neon/Supabase)  
  

⭐ If you like this project, consider starring the repository!
