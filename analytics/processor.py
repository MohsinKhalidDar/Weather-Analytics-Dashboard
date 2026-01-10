def extract_features(raw: dict) -> dict:
    """
    Extracts clean, meaningful metrics from raw API response.
    """
    return {
        "city": raw["name"],
        "temperature": raw["main"]["temp"],
        "feels_like": raw["main"]["feels_like"],
        "humidity": raw["main"]["humidity"],
        "pressure": raw["main"]["pressure"],
        "wind_speed": raw["wind"]["speed"],
        "condition": raw["weather"][0]["main"]
    }
