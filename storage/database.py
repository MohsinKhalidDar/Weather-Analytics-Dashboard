import sqlite3
import pandas as pd
from storage.models import CREATE_WEATHER_TABLE

DB_PATH = "storage/weather.db"


# ---------------------------
# Connection
# ---------------------------
def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute(CREATE_WEATHER_TABLE)
    create_forecast_table(conn)
    return conn


# ---------------------------
# Current & Historical Weather
# ---------------------------
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


# ---------------------------
# Forecast Cache
# ---------------------------
def create_forecast_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS weather_forecast (
            city TEXT,
            date TEXT,
            min_temp REAL,
            max_temp REAL,
            avg_temp REAL,
            fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()


def insert_forecast(conn, city: str, df: pd.DataFrame):
    # Remove old forecast for city
    conn.execute("DELETE FROM weather_forecast WHERE city = ?", (city,))

    for _, row in df.iterrows():
        conn.execute("""
            INSERT INTO weather_forecast
            (city, date, min_temp, max_temp, avg_temp)
            VALUES (?, ?, ?, ?, ?)
        """, (
            city,
            pd.to_datetime(row["date"]).strftime("%Y-%m-%d"),
            row["min_temp"],
            row["max_temp"],
            row["avg_temp"]
        ))

    conn.commit()


def fetch_cached_forecast(conn, city: str):
    cursor = conn.execute("""
        SELECT date, min_temp, max_temp, avg_temp
        FROM weather_forecast
        WHERE city = ?
        ORDER BY date
    """, (city,))

    rows = cursor.fetchall()

    if not rows:
        return None

    df = pd.DataFrame(
        rows,
        columns=["date", "min_temp", "max_temp", "avg_temp"]
    )
    df["date"] = pd.to_datetime(df["date"])
    return df
