import streamlit as st

from services.weather_api import fetch_weather, WeatherAPIError
from analytics.processor import extract_features
from analytics.indicators import comfort_index, wind_risk
from analytics.health_scores import weather_health_score
from utils.validators import validate_city

st.set_page_config(
    page_title="Weather Analytics Dashboard",
    layout="wide"
)

st.title("🌦️ Weather Analytics Dashboard")
st.caption("Industry-grade, analytics-first weather intelligence")

# Sidebar
with st.sidebar:
    st.header("Controls")
    city = st.text_input("Enter city name")
    analyze = st.button("Analyze Weather")

if analyze:
    try:
        validate_city(city)

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
        st.write(features)  # TEMP: we will replace this with KPIs & charts

    except WeatherAPIError as e:
        st.error(str(e))

    except ValueError as e:
        st.warning(str(e))
