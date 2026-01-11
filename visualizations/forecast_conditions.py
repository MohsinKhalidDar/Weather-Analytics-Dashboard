import streamlit as st


def render_forecast_conditions(df):
    """
    Render daily weather conditions safely.
    Works for both live and cached forecast data.
    """

    if "condition" not in df.columns:
        st.info(
            "Weather condition details are available "
            "only for live forecast data."
        )
        return

    st.subheader("Daily Weather Outlook")

    cols = st.columns(len(df))

    for col, (_, row) in zip(cols, df.iterrows()):
        with col:
            st.markdown(
                f"""
                **{row['date'].strftime('%b %d')}**  
                {row['condition']}
                """,
                unsafe_allow_html=True
            )
