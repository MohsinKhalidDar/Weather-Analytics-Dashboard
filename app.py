from services.weather_api import fetch_weather
from analytics.processor import extract_features
from analytics.indicators import comfort_index, wind_risk
from analytics.health_scores import weather_health_score

city = "London"

raw = fetch_weather(city)
features = extract_features(raw)

features["comfort"] = comfort_index(
    features["temperature"],
    features["humidity"]
)

features["wind_risk"] = wind_risk(
    features["temperature"],
    features["wind_speed"]
)

features["health"] = weather_health_score(features)

print(features)
