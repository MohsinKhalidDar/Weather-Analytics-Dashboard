def condition_to_emoji(condition: str) -> str:
    """
    Map WeatherAPI condition text to an emoji icon.
    """
    if not condition:
        return "🌡️"

    c = condition.lower()

    if "sun" in c or "clear" in c:
        return "☀️"
    if "cloud" in c or "overcast" in c:
        return "☁️"
    if "rain" in c or "drizzle" in c or "shower" in c or "patchy" in c:
        return "🌧️"     
    if "thunder" in c or "storm" in c:
        return "⛈️"
    if "snow" in c or "blizzard" in c or "sleet" in c:
        return "❄️"
    if "mist" in c or "fog" in c or "haze" in c:
        return "🌫️"

    return "🌡️"
