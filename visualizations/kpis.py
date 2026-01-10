import streamlit as st

def render_kpis(features: dict):
    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("🌡 Temperature (°C)", f"{features['temperature']:.1f}")
    c2.metric("🤒 Feels Like (°C)", f"{features['feels_like']:.1f}")
    c3.metric("💧 Humidity (%)", f"{features['humidity']}")
    c4.metric("🌬 Wind (m/s)", f"{features['wind_speed']}")
    c5.metric("🏥 Health Score", f"{features['health']}")
