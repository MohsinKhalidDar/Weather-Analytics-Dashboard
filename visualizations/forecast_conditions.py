import streamlit as st


def render_forecast_conditions(df):
    """
    Render daily weather conditions safely.
    Works for both live and cached forecast data.
    """

    st.subheader("🌤️ Daily Weather Outlook")

    # Cached data safety (no condition info)
    has_conditions = "condition" in df.columns
    has_icons = "icon" in df.columns
    has_rain = "rain_prob" in df.columns

    cols = st.columns(len(df))

    for col, (_, row) in zip(cols, df.iterrows()):
        with col:
            # Date
            st.markdown(
                f"**{row['date'].strftime('%a, %b %d')}**"
            )

            # Icon (live forecast only)
            if has_icons:
                st.image(row["icon"], width=48)

            # Condition text
            if has_conditions:
                st.caption(row["condition"])

            # Temperature summary
            st.markdown(
                f"""
                🌡️ **{row['avg_temp']}°C**  
                <small>Min: {row['min_temp']}° | Max: {row['max_temp']}°</small>
                """,
                unsafe_allow_html=True
            )

            # Rain probability (live forecast only)
            if has_rain:
                st.progress(row["rain_prob"] / 100)
                st.caption(f"🌧️ Rain chance: {row['rain_prob']}%")
