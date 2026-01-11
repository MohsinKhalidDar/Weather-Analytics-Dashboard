import os
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = os.getenv("BASE_URL")

WEATHERAPI_KEY = os.getenv("WEATHERAPI_KEY")
WEATHERAPI_BASE_URL = os.getenv("WEATHERAPI_BASE_URL")

REQUEST_TIMEOUT = 25
