import pandas as pd


def process_weatherapi_forecast(forecast_json: dict) -> pd.DataFrame:
    """
    Process WeatherAPI daily forecast response into an analytics-ready DataFrame.

    Expected WeatherAPI structure:
    forecast
      └── forecastday
            └── day
                ├── mintemp_c
                ├── maxtemp_c
                ├── avgtemp_c

    Output DataFrame columns:
    - date (datetime)
    - min_temp (°C)
    - max_temp (°C)  -> daytime temperature
    - avg_temp (°C)
    """

    # ---------------------------
    # Validation
    # ---------------------------
    if (
        "forecast" not in forecast_json
        or "forecastday" not in forecast_json["forecast"]
    ):
        raise ValueError("Invalid WeatherAPI forecast format")

    records = []

    # ---------------------------
    # Extraction
    # ---------------------------
    for day in forecast_json["forecast"]["forecastday"]:
        records.append({
            "date": day["date"],
            "min_temp": day["day"]["mintemp_c"],
            "max_temp": day["day"]["maxtemp_c"],
            "avg_temp": day["day"]["avgtemp_c"],
        })

    # ---------------------------
    # Transformation
    # ---------------------------
    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df["date"])

    return df
