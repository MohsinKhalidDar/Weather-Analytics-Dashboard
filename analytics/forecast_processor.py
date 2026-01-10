from datetime import datetime
import pandas as pd


def process_daily_forecast(forecast_json: dict) -> pd.DataFrame:
    """
    Convert raw forecast API response into a clean analytics dataframe.

    Output columns:
    - date
    - min_temp
    - max_temp
    - avg_temp
    - humidity
    - wind_speed
    """

    if "list" not in forecast_json:
        raise ValueError("Invalid forecast data format")

    records = []

    for day in forecast_json["list"]:
        record = {
            "date": datetime.fromtimestamp(day["dt"]).date(),
            "min_temp": day["temp"]["min"],
            "max_temp": day["temp"]["max"],
            "avg_temp": round(
                (day["temp"]["min"] + day["temp"]["max"]) / 2, 2
            ),
            "humidity": day["humidity"],
            "wind_speed": day["speed"],
        }
        records.append(record)

    df = pd.DataFrame(records)
    return df
