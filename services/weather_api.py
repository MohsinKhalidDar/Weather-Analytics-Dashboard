import requests
from config.settings import (
    WEATHER_API_KEY,
    BASE_URL,
    WEATHERAPI_KEY,
    WEATHERAPI_BASE_URL,
    REQUEST_TIMEOUT
)


class WeatherAPIError(Exception):
    """Custom exception for weather API failures"""
    pass


# -----------------------------
# OpenWeather — current weather
# -----------------------------
def fetch_weather(city: str) -> dict:
    if not WEATHER_API_KEY:
        raise WeatherAPIError("Missing OpenWeather API key")

    url = f"{BASE_URL}/weather"
    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)

        if response.status_code != 200:
            raise WeatherAPIError(
                response.json().get("message", "Weather API error")
            )

        return response.json()

    except requests.exceptions.Timeout:
        raise WeatherAPIError("Weather API request timed out")

    except requests.exceptions.RequestException:
        raise WeatherAPIError("Network error while calling Weather API")


# -----------------------------
# WeatherAPI — daily forecast
# -----------------------------
import time

def fetch_daily_forecast_weatherapi(city: str, days: int = 5) -> dict:
    if not WEATHERAPI_KEY:
        raise WeatherAPIError("Missing WeatherAPI key")

    params = {
        "key": WEATHERAPI_KEY,
        "q": city,
        "days": days,
        "aqi": "no",
        "alerts": "no"
    }

    last_error = None

    for attempt in range(3):  # retry 3 times
        try:
            response = requests.get(
                f"{WEATHERAPI_BASE_URL}/forecast.json",
                params=params,
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.Timeout as e:
            last_error = e
            time.sleep(1)  # small backoff

        except requests.exceptions.RequestException as e:
            raise WeatherAPIError(
                f"WeatherAPI request failed: {str(e)}"
            )

    raise WeatherAPIError("WeatherAPI forecast request timed out after retries")
 