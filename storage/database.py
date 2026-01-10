import sqlite3
from storage.models import CREATE_WEATHER_TABLE

DB_PATH = "storage/weather.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute(CREATE_WEATHER_TABLE)
    return conn


def insert_weather(conn, data: dict):
    query = """
    INSERT INTO weather_history (
        city, temperature, feels_like,
        humidity, pressure, wind_speed,
        condition, comfort, health
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    conn.execute(query, (
        data["city"],
        data["temperature"],
        data["feels_like"],
        data["humidity"],
        data["pressure"],
        data["wind_speed"],
        data["condition"],
        data["comfort"],
        data["health"]
    ))
    conn.commit()

def fetch_weather_history(city: str, limit: int = 200):
    conn = get_connection()

    query = """
    SELECT
        datetime(timestamp) AS timestamp,
        temperature,
        health
    FROM weather_history
    WHERE city = ?
    ORDER BY timestamp ASC
    LIMIT ?
    """

    rows = conn.execute(query, (city, limit)).fetchall()
    return rows
