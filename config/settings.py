import os
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = os.getenv("BASE_URL")

REQUEST_TIMEOUT = 10
