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
CREATE_FORECAST_ACCURACY_TABLE = """
CREATE TABLE IF NOT EXISTS forecast_accuracy (
    city TEXT,
    date TEXT,
    predicted_avg REAL,
    actual_avg REAL,
    abs_error REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""
