import pandas as pd


def process_weatherapi_forecast(forecast_json: dict) -> pd.DataFrame:
    """
    Convert WeatherAPI daily forecast response into a clean DataFrame.

    Expected output columns:
    - date
    - min_temp
    - max_temp
    - avg_temp
    - condition
    - icon
    - rain_prob
    """

    # Safety check
    if "forecast" not in forecast_json or "forecastday" not in forecast_json["forecast"]:
        raise ValueError("Invalid WeatherAPI forecast format")

    records = []

    for day in forecast_json["forecast"]["forecastday"]:
        records.append({
            "date": pd.to_datetime(day["date"]),
            "min_temp": day["day"]["mintemp_c"],
            "max_temp": day["day"]["maxtemp_c"],
            "avg_temp": day["day"]["avgtemp_c"],
            "condition": day["day"]["condition"]["text"],
            "icon": "https:" + day["day"]["condition"]["icon"],
            "rain_prob": int(day["day"]["daily_chance_of_rain"]),
        })

    df = pd.DataFrame(records)

    # -------------------------
    # Schema validation (SAFE)
    # -------------------------
    expected_cols = {
        "date",
        "min_temp",
        "max_temp",
        "avg_temp",
        "condition",
        "icon",
        "rain_prob",
    }

    missing = expected_cols - set(df.columns)
    if missing:
        raise ValueError(
            f"Forecast processor missing columns: {missing}"
        )

    return df
