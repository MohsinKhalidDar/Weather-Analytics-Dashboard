import streamlit as st
from datetime import datetime, timedelta
import time

from config.settings import WEATHER_API_KEY, WEATHERAPI_KEY


# =========================
# Core services & analytics
# =========================
from services.weather_api import (
    fetch_weather,
    fetch_daily_forecast_weatherapi,
    WeatherAPIError
)

from analytics.processor import extract_features
from analytics.indicators import comfort_index, wind_risk
from analytics.health_scores import weather_health_score
from analytics.weatherapi_forecast_processor import process_weatherapi_forecast
from analytics.alerts import generate_weather_alerts
from analytics.accuracy import compute_mae, prepare_accuracy_df

from utils.validators import validate_city


# =========================
# Visualization layer
# =========================
from visualizations.kpis import render_kpis
from visualizations.charts import (
    temp_comparison_chart,
    radar_weather_chart,
    historical_trend_charts
)
from visualizations.forecast_charts import forecast_temperature_chart
from visualizations.forecast_conditions import render_forecast_conditions
from visualizations.accuracy_charts import accuracy_trend_chart


# =========================
# Storage layer
# =========================
from storage.database import (
    get_connection,
    insert_weather,
    fetch_weather_history,
    insert_forecast,
    fetch_cached_forecast,
    fetch_yesterday_forecast,
    insert_forecast_accuracy,
    fetch_forecast_accuracy
)


# =========================
# Cached DB connection
# =========================
@st.cache_resource
def get_db():
    return get_connection()


# =========================
# Helpers (Latency + time formatting)
# =========================
def latency_badge(latency: float | None, warn: float, critical: float) -> str:
    if latency is None:
        return "⚪ Not measured yet"

    if latency < warn:
        return f"🟢 Fast ({latency:.2f}s)"

    if latency < critical:
        return f"🟡 Slow ({latency:.2f}s)"

    return f"🔴 Critical ({latency:.2f}s)"


def format_time(ts: float | None) -> str:
    if ts is None:
        return "—"
    return datetime.fromtimestamp(ts).strftime("%I:%M:%S %p")


def render_perf_sidebar(perf_box):
    """
    Render sidebar API performance with:
    - Live latency badge + timestamp
    - Forecast latency badge + timestamp
    - Shows "Failed / Timeout" if forecast attempted but failed
    """
    live_latency = st.session_state.get("live_latency")
    forecast_latency = st.session_state.get("forecast_latency")

    live_updated_at = st.session_state.get("live_updated_at")
    forecast_updated_at = st.session_state.get("forecast_updated_at")

    live_text = latency_badge(live_latency, warn=2, critical=4)
    forecast_text = latency_badge(forecast_latency, warn=3, critical=6)

    # ✅ If forecast was attempted but failed
    if forecast_latency is None and forecast_updated_at is not None:
        forecast_text = "🔴 Failed / Timeout"

    perf_box.markdown(
        f"""
        **Live Weather:** {live_text}  
        <small>Last updated: {format_time(live_updated_at)}</small>

        **Forecast:** {forecast_text}  
        <small>Last updated: {format_time(forecast_updated_at)}</small>
        """,
        unsafe_allow_html=True
    )


# =========================
# Page config
# =========================
st.set_page_config(
    page_title="Weather Analytics Dashboard",
    layout="wide"
)

st.title("🌦️ Weather Analytics Dashboard")
st.caption("Industry-grade, analytics-first weather intelligence")


# =========================
# Session state defaults
# =========================
if "live_latency" not in st.session_state:
    st.session_state["live_latency"] = None

if "forecast_latency" not in st.session_state:
    st.session_state["forecast_latency"] = None

if "live_updated_at" not in st.session_state:
    st.session_state["live_updated_at"] = None

if "forecast_updated_at" not in st.session_state:
    st.session_state["forecast_updated_at"] = None

if "last_city" not in st.session_state:
    st.session_state["last_city"] = ""


# =========================
# Sidebar controls
# =========================
with st.sidebar:
    st.header("Controls")

    city = st.text_input("Enter city name", value=st.session_state["last_city"])

    col1, col2 = st.columns(2)

    with col1:
        analyze = st.button("Analyze Weather")

    with col2:
        refresh = st.button("🔄 Refresh")

    # ✅ Refresh triggers analysis again using saved city
    if refresh:
        if st.session_state["last_city"]:
            city = st.session_state["last_city"]
            analyze = True
        else:
            st.warning("No previous city found. Please analyze once first.")

    st.markdown("---")
    st.subheader("🔐 API Status")

    if WEATHER_API_KEY:
        st.success("OpenWeather Key: Loaded ✅")
    else:
        st.error("OpenWeather Key: Missing ❌")

    if WEATHERAPI_KEY:
        st.success("WeatherAPI Key: Loaded ✅")
    else:
        st.error("WeatherAPI Key: Missing ❌")

    st.markdown("---")
    st.subheader("📡 API Performance")

    perf_box = st.empty()
    render_perf_sidebar(perf_box)


# =========================
# Main logic
# =========================
if analyze:
    try:
        # -----------------------------
        # Validate input
        # -----------------------------
        validate_city(city)

        # ✅ Save city in session so refresh works
        st.session_state["last_city"] = city

        # -----------------------------
        # STEP 5: Live Weather API latency monitoring
        # -----------------------------
        with st.spinner("Fetching live weather data..."):
            start = time.time()
            raw = fetch_weather(city)
            live_latency = time.time() - start

            # ✅ Store latency + update time
            st.session_state["live_latency"] = live_latency
            st.session_state["live_updated_at"] = time.time()

            # ✅ Update sidebar instantly
            render_perf_sidebar(perf_box)

            if live_latency > 2:
                st.warning("⚠️ Live weather service is slower than usual")

            features = extract_features(raw)

            features["comfort"] = comfort_index(
                features["temperature"], features["humidity"]
            )
            features["wind_risk"] = wind_risk(
                features["temperature"], features["wind_speed"]
            )
            features["health"] = weather_health_score(features)

        st.success(f"Weather analysis for {features['city']}")

        # -----------------------------
        # Store snapshot in SQLite
        # -----------------------------
        conn = get_db()
        insert_weather(conn, features)

        # ==================================================
        # Forecast Accuracy Tracking (Actual vs Predicted)
        # ==================================================
        today = datetime.utcnow().date()
        yesterday = today - timedelta(days=1)
        # For testing ONLY:
        # yesterday = today

        predicted_avg = fetch_yesterday_forecast(
            conn,
            features["city"],
            yesterday.strftime("%Y-%m-%d")
        )

        if predicted_avg is not None:
            insert_forecast_accuracy(
                conn,
                features["city"],
                yesterday.strftime("%Y-%m-%d"),
                predicted_avg=predicted_avg,
                actual_avg=features["temperature"]
            )

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

        # =============================
        # Forecast Model Performance
        # =============================
        st.markdown("---")
        st.subheader("📊 Forecast Model Performance")

        accuracy_rows = fetch_forecast_accuracy(conn, features["city"])
        mae = compute_mae(accuracy_rows)

        if mae is not None:
            st.metric("📉 Forecast MAE (°C)", mae)

        accuracy_df = prepare_accuracy_df(accuracy_rows)

        if accuracy_df is not None and len(accuracy_df) >= 2:
            acc_fig = accuracy_trend_chart(accuracy_df)
            st.plotly_chart(acc_fig, use_container_width=True)
        else:
            st.info(
                "Forecast accuracy trend will appear after multiple days "
                "of forecast evaluation."
            )

        # =============================
        # STEP 6: Forecast API latency monitoring
        # =============================
        forecast_df = None
        forecast_source = None

        try:
            with st.spinner("Fetching weather forecast..."):
                start = time.time()
                forecast_raw = fetch_daily_forecast_weatherapi(
                    features["city"], days=5
                )
                forecast_latency = time.time() - start

                # ✅ Store forecast latency + update time
                st.session_state["forecast_latency"] = forecast_latency
                st.session_state["forecast_updated_at"] = time.time()

                # ✅ Update sidebar instantly
                render_perf_sidebar(perf_box)

                if forecast_latency > 3:
                    st.warning("⚠️ Forecast service is slower than usual")

                forecast_df = process_weatherapi_forecast(forecast_raw)

                # Cache successful forecast
                insert_forecast(conn, features["city"], forecast_df)
                forecast_source = "Live forecast data"

        except WeatherAPIError:
            # ✅ Even on fail, mark forecast as "attempted" so sidebar updates
            st.session_state["forecast_latency"] = None
            st.session_state["forecast_updated_at"] = time.time()
            render_perf_sidebar(perf_box)

            # Try cached forecast
            forecast_df = fetch_cached_forecast(conn, features["city"])

            if forecast_df is not None:
                forecast_source = (
                    "Using last cached forecast "
                    "(API temporarily unavailable)"
                )
            else:
                forecast_source = None

        # -----------------------------
        # Smart Weather Alerts
        # -----------------------------
        if forecast_df is not None:
            alerts = generate_weather_alerts(forecast_df)

            if alerts:
                st.markdown("---")
                st.subheader("⚠️ Weather Alerts")

                for alert in alerts:
                    st.warning(alert)

        # -----------------------------
        # Render Forecast UI
        # -----------------------------
        if forecast_df is not None:
            st.markdown("---")
            st.subheader("Weather Forecast (Next 5 Days)")
            st.caption(forecast_source)

            forecast_fig = forecast_temperature_chart(forecast_df)
            st.plotly_chart(forecast_fig, use_container_width=True)

            st.markdown("### Weather Conditions")
            render_forecast_conditions(forecast_df)

        else:
            st.markdown("---")
            st.warning(
                "Forecast service is currently unavailable and no cached data exists yet.\n\n"
                "Try again later to build forecast cache."
            )

    except WeatherAPIError as e:
        st.warning(
            "Weather service is temporarily slow.\n\n"
            f"Details: {e}"
        )

    except ValueError as e:
        st.warning(str(e))
