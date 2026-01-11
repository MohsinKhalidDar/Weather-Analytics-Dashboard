import streamlit as st

 
# Core services & analytics

from services.weather_api import fetch_daily_forecast_weatherapi
from analytics.weatherapi_forecast_processor import process_weatherapi_forecast
from visualizations.forecast_charts import forecast_temperature_chart

 
from services.weather_api import fetch_weather, WeatherAPIError
from analytics.processor import extract_features
from analytics.indicators import comfort_index, wind_risk
from analytics.health_scores import weather_health_score
from utils.validators import validate_city

 
# Visualization layer
 
from visualizations.kpis import render_kpis
from visualizations.charts import (
    temp_comparison_chart,
    radar_weather_chart,
    historical_trend_charts
)

# Storage layer
from storage.database import get_connection, insert_weather, fetch_weather_history
from storage.database import insert_forecast, fetch_cached_forecast

 
# Cached DB connection
 
@st.cache_resource
def get_db():
    return get_connection()


# Page config
 
st.set_page_config(
    page_title="Weather Analytics Dashboard",
    layout="wide"
)

st.title("🌦️ Weather Analytics Dashboard")
st.caption("Industry-grade, analytics-first weather intelligence")

 
# Sidebar controls
 
with st.sidebar:
    st.header("Controls")
    city = st.text_input("Enter city name")
    analyze = st.button("Analyze Weather")


 
# Main logic
 
if analyze:
    try:
        # Validate input
        validate_city(city)

        # Fetch & process live weather
        with st.spinner("Fetching live weather data..."):
            raw = fetch_weather(city)
            features = extract_features(raw)

            features["comfort"] = comfort_index(
                features["temperature"], features["humidity"]
            )
            features["wind_risk"] = wind_risk(
                features["temperature"], features["wind_speed"]
            )
            features["health"] = weather_health_score(features)

        st.success(f"Weather analysis for {features['city']}")

        # Store snapshot in SQLite
        conn = get_db()
        insert_weather(conn, features)

        # -----------------------------
        # KPI Section
        # -----------------------------
        st.subheader("Key Metrics")
        render_kpis(features)

        st.markdown("---")

        # -----------------------------
        # Comparison Charts
        # -----------------------------
        left, right = st.columns(2)

        with left:
            st.plotly_chart(
                temp_comparison_chart(features),
                use_container_width=True
            )

        with right:
            st.plotly_chart(
                radar_weather_chart(features),
                use_container_width=True
            )

        st.markdown("---")

        # -----------------------------
        # Historical Trends
        # -----------------------------
        st.subheader("Historical Trends")

        history_rows = fetch_weather_history(features["city"])
        temp_fig, health_fig = historical_trend_charts(history_rows)

        if temp_fig and health_fig:
            c1, c2 = st.columns(2)

            with c1:
                st.plotly_chart(temp_fig, use_container_width=True)

            with c2:
                st.plotly_chart(health_fig, use_container_width=True)
        else:
            st.info(
                "Not enough historical data yet. "
                "Analyze this city multiple times to build trends."
            )
            
        st.markdown("---")
        st.subheader("Weather Forecast (Next 5 Days)")

        st.markdown("---")
        st.subheader("Weather Forecast (Next 5 Days)")

        conn = get_db()

        try:
            with st.spinner("Fetching weather forecast..."):
                forecast_raw = fetch_daily_forecast_weatherapi(features["city"], days=5)
                forecast_df = process_weatherapi_forecast(forecast_raw)

                # Cache successful forecast
                insert_forecast(conn, features["city"], forecast_df)
                st.caption("Live forecast data")

        except WeatherAPIError:
            forecast_df = fetch_cached_forecast(conn, features["city"])

            if forecast_df is not None:
                st.caption("Using last cached forecast (API temporarily unavailable)")
            else:
                st.warning("Forecast service unavailable and no cached data found.")
                forecast_df = None

        if forecast_df is not None:
            forecast_fig = forecast_temperature_chart(forecast_df)
            st.plotly_chart(forecast_fig, use_container_width=True)
 
            

    except WeatherAPIError as e:
        st.warning(
            "Forecast service is temporarily slow. "
            "Live and historical data are still available.\n\n"
            f"Details: {e}"
    )


    except ValueError as e:
        st.warning(str(e))
