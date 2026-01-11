import pandas as pd


def process_weatherapi_forecast(forecast_json: dict) -> pd.DataFrame:
    """
    Convert WeatherAPI daily forecast response into a clean DataFrame.
    """

    # Safety check
    if "forecast" not in forecast_json or "forecastday" not in forecast_json["forecast"]:
        raise ValueError("Invalid WeatherAPI forecast format")

    records = []

    for day in forecast_json["forecast"]["forecastday"]:
        records.append({
            "date": day["date"],
            "min_temp": day["day"]["mintemp_c"],
            "max_temp": day["day"]["maxtemp_c"],
            "avg_temp": day["day"]["avgtemp_c"],
            "humidity": day["day"]["avghumidity"],
            "condition": day["day"]["condition"]["text"]
        })

    df = pd.DataFrame(records)
    return df
