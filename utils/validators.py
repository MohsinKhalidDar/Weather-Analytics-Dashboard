def validate_city(city: str):
    if not city or len(city.strip()) < 2:
        raise ValueError("City name is invalid")
