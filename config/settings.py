import os

# ✅ Load local .env if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "20"))

BASE_URL = os.getenv("BASE_URL", "https://api.openweathermap.org/data/2.5")
WEATHERAPI_BASE_URL = os.getenv("WEATHERAPI_BASE_URL", "https://api.weatherapi.com/v1")

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHERAPI_KEY = os.getenv("WEATHERAPI_KEY")

# ✅ Streamlit Cloud fallback (safe)
try:
    import streamlit as st

    WEATHER_API_KEY = WEATHER_API_KEY or st.secrets.get("WEATHER_API_KEY", None)
    WEATHERAPI_KEY = WEATHERAPI_KEY or st.secrets.get("WEATHERAPI_KEY", None)

    BASE_URL = st.secrets.get("BASE_URL", BASE_URL)
    WEATHERAPI_BASE_URL = st.secrets.get("WEATHERAPI_BASE_URL", WEATHERAPI_BASE_URL)

    REQUEST_TIMEOUT = int(str(st.secrets.get("REQUEST_TIMEOUT", REQUEST_TIMEOUT)))

except Exception:
    pass
