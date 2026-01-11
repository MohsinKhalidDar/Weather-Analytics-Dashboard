import pandas as pd


def generate_weather_alerts(forecast_df: pd.DataFrame) -> list[str]:
    """
    Generate weather alerts based on forecast thresholds.
    Returns a list of alert messages.
    """

    alerts = []

    # -----------------------
    # Heatwave alert
    # -----------------------
    if "max_temp" in forecast_df.columns:
        hot_days = forecast_df[forecast_df["max_temp"] >= 40]

        if not hot_days.empty:
            days = ", ".join(
                hot_days["date"].dt.strftime("%A")
            )
            alerts.append(
                f"🔥 Heatwave alert: Very high temperatures expected on {days}."
            )

    # -----------------------
    # Cold wave alert
    # -----------------------
    cold_days = forecast_df[forecast_df["min_temp"] <= 5]

    if not cold_days.empty:
        days = ", ".join(
            cold_days["date"].dt.strftime("%A")
        )
        alerts.append(
            f"❄️ Cold wave alert: Extremely low temperatures expected on {days}."
        )

    # -----------------------
    # Heavy rain alert
    # -----------------------
    if "rain_prob" in forecast_df.columns:
        rainy_days = forecast_df[forecast_df["rain_prob"] >= 70]

        if not rainy_days.empty:
            days = ", ".join(
                rainy_days["date"].dt.strftime("%A")
            )
            alerts.append(
                f"🌧️ Heavy rain alert: High chance of rain on {days}."
            )

    return alerts
