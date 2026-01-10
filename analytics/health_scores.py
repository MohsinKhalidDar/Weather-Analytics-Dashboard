def weather_health_score(features: dict) -> int:
    score = 100

    if features["humidity"] > 80:
        score -= 15

    if features["wind_speed"] > 10:
        score -= 10

    if features["temperature"] < 5 or features["temperature"] > 38:
        score -= 25

    return max(score, 0)
