import time
import requests

from utils.logger import setup_logger
from config.settings import (
    WEATHER_API_KEY,
    BASE_URL,
    WEATHERAPI_KEY,
    WEATHERAPI_BASE_URL,
    REQUEST_TIMEOUT
)

logger = setup_logger()


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

    logger.info(f"[OpenWeather] Fetching current weather | city={city}")

    try:
        start = time.time()
        response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
        latency = time.time() - start

        logger.info(f"[OpenWeather] Response received | city={city} | latency={latency:.2f}s")

        if response.status_code != 200:
            msg = response.json().get("message", "Weather API error")
            logger.warning(f"[OpenWeather] Non-200 response | city={city} | status={response.status_code} | msg={msg}")
            raise WeatherAPIError(msg)

        return response.json()

    except requests.exceptions.Timeout:
        logger.warning(f"[OpenWeather] Timeout | city={city}")
        raise WeatherAPIError("Weather API request timed out")

    except requests.exceptions.RequestException as e:
        logger.error(f"[OpenWeather] Network error | city={city} | error={str(e)}")
        raise WeatherAPIError("Network error while calling Weather API")


# -----------------------------
# WeatherAPI — daily forecast
# -----------------------------
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

    logger.info(f"[WeatherAPI] Fetching daily forecast | city={city} | days={days}")

    last_error = None

    for attempt in range(1, 4):  # attempts: 1..3
        try:
            start = time.time()
            response = requests.get(
                f"{WEATHERAPI_BASE_URL}/forecast.json",
                params=params,
                timeout=REQUEST_TIMEOUT
            )
            latency = time.time() - start

            logger.info(
                f"[WeatherAPI] Attempt {attempt} success | city={city} | latency={latency:.2f}s"
            )

            response.raise_for_status()
            return response.json()

        except requests.exceptions.Timeout as e:
            last_error = e
            logger.warning(
                f"[WeatherAPI] Timeout on attempt {attempt} | city={city} | retrying..."
            )
            time.sleep(1)  # backoff

        except requests.exceptions.RequestException as e:
            logger.error(
                f"[WeatherAPI] Request failed | city={city} | attempt={attempt} | error={str(e)}"
            )
            raise WeatherAPIError(f"WeatherAPI request failed: {str(e)}")

    logger.error(
        f"[WeatherAPI] Forecast timed out after retries | city={city} | last_error={str(last_error)}"
    )
    raise WeatherAPIError("WeatherAPI forecast request timed out after retries")
