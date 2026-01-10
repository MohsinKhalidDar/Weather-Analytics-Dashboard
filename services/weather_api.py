import requests
from config.settings import WEATHER_API_KEY, BASE_URL, REQUEST_TIMEOUT


class WeatherAPIError(Exception):
    """Custom exception for weather API failures"""
    pass


def fetch_weather(city: str) -> dict:
    if not WEATHER_API_KEY:
        raise WeatherAPIError("Missing API key")

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
