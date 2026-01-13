import streamlit as st
import pandas as pd
from utils.weather_emojis import condition_to_emoji


def render_forecast_conditions(df):
    """
    Render daily weather conditions safely.
    Works for both live and cached forecast data.
    """

    st.subheader("🌤️ Daily Weather Outlook")

    has_conditions = "condition" in df.columns
    has_icons = "icon" in df.columns
    has_rain = "rain_prob" in df.columns

    cols = st.columns(len(df))

    for col, (_, row) in zip(cols, df.iterrows()):
        with col:
            st.markdown(f"**{row['date'].strftime('%a, %b %d')}**")

            condition_text = row.get("condition", "") if has_conditions else ""
            emoji = condition_to_emoji(condition_text)
            st.markdown(f"{emoji}")

            if has_icons and pd.notna(row.get("icon")):
                st.image(row["icon"], width=48)

            if has_conditions:
                st.caption(row.get("condition", "N/A"))

            st.markdown(
                f"""
                🌡️ **{row['avg_temp']}°C**  
                <small>Min: {row['min_temp']}° | Max: {row['max_temp']}°</small>
                """,
                unsafe_allow_html=True
            )

            if has_rain and pd.notna(row.get("rain_prob")):
                rain_val = int(row["rain_prob"])
                st.progress(rain_val / 100)
                st.caption(f"🌧️ Rain chance: {rain_val}%")
