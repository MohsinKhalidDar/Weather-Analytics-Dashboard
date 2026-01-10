def comfort_index(temp: float, humidity: int) -> float:
    """
    Comfort score between 0 and 100.
    """
    score = 100 - abs(temp - 22) * 2 - abs(humidity - 50) * 0.5
    return round(max(min(score, 100), 0), 2)


def wind_risk(temp: float, wind_speed: float) -> str:
    if temp < 10 and wind_speed > 6:
        return "High"
    elif temp < 15:
        return "Moderate"
    return "Low"
