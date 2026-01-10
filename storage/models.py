CREATE_WEATHER_TABLE = """
CREATE TABLE IF NOT EXISTS weather_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city TEXT,
    temperature REAL,
    feels_like REAL,
    humidity INTEGER,
    pressure INTEGER,
    wind_speed REAL,
    condition TEXT,
    comfort REAL,
    health INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""
