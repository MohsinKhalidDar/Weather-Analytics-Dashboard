import sqlite3
import pandas as pd
from storage.models import (
    CREATE_WEATHER_TABLE,
    CREATE_FORECAST_ACCURACY_TABLE
)

DB_PATH = "storage/weather.db"


# ==================================================
# Connection
# ==================================================
def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute(CREATE_WEATHER_TABLE)
    create_forecast_table(conn)
    conn.execute(CREATE_FORECAST_ACCURACY_TABLE)
    return conn


# ==================================================
# Current & Historical Weather
# ==================================================
def insert_weather(conn, data: dict):
    query = """
    INSERT INTO weather_history (
        city,
        temperature,
        feels_like,
        humidity,
        pressure,
        wind_speed,
        condition,
        comfort,
        health
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    conn.execute(
        query,
        (
            data["city"],
            data["temperature"],
            data["feels_like"],
            data["humidity"],
            data["pressure"],
            data["wind_speed"],
            data["condition"],
            data["comfort"],
            data["health"],
        ),
    )
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


# ==================================================
# Forecast Cache (WITH CONDITIONS + ICON + RAIN_PROB)
# ==================================================
def create_forecast_table(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS weather_forecast (
            city TEXT,
            date TEXT,
            min_temp REAL,
            max_temp REAL,
            avg_temp REAL,
            condition TEXT,
            icon TEXT,
            rain_prob INTEGER,
            fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()


def insert_forecast(conn, city: str, df: pd.DataFrame):
    """
    Cache forecast for a city.
    Old forecast is replaced to keep cache fresh.
    """

    conn.execute("DELETE FROM weather_forecast WHERE city = ?", (city,))

    for _, row in df.iterrows():
        conn.execute(
            """
            INSERT INTO weather_forecast (
                city,
                date,
                min_temp,
                max_temp,
                avg_temp,
                condition,
                icon,
                rain_prob
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                city,
                pd.to_datetime(row["date"]).strftime("%Y-%m-%d"),
                row["min_temp"],
                row["max_temp"],
                row["avg_temp"],
                row.get("condition"),
                row.get("icon"),
                row.get("rain_prob"),
            ),
        )

    conn.commit()


def fetch_cached_forecast(conn, city: str):
    cursor = conn.execute(
        """
        SELECT
            date,
            min_temp,
            max_temp,
            avg_temp,
            condition,
            icon,
            rain_prob
        FROM weather_forecast
        WHERE city = ?
        ORDER BY date
        """,
        (city,),
    )

    rows = cursor.fetchall()

    if not rows:
        return None

    df = pd.DataFrame(
        rows,
        columns=[
            "date",
            "min_temp",
            "max_temp",
            "avg_temp",
            "condition",
            "icon",
            "rain_prob",
        ],
    )

    df["date"] = pd.to_datetime(df["date"])
    return df


# ==================================================
# Forecast Accuracy (STEP 4)
# ==================================================
def fetch_yesterday_forecast(conn, city: str, date: str):
    cursor = conn.execute(
        """
        SELECT avg_temp
        FROM weather_forecast
        WHERE city = ? AND date = ?
        """,
        (city, date),
    )

    row = cursor.fetchone()
    return row[0] if row else None


def insert_forecast_accuracy(
    conn,
    city: str,
    date: str,
    predicted_avg: float,
    actual_avg: float
):
    """
    Insert forecast accuracy row.
    ✅ Idempotent: removes any existing record for same (city, date).
    """

    abs_error = abs(predicted_avg - actual_avg)

    # ✅ Avoid duplicates on repeated runs
    conn.execute(
        """
        DELETE FROM forecast_accuracy
        WHERE city = ? AND date = ?
        """,
        (city, date),
    )

    conn.execute(
        """
        INSERT INTO forecast_accuracy
        (city, date, predicted_avg, actual_avg, abs_error)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            city,
            date,
            predicted_avg,
            actual_avg,
            abs_error,
        ),
    )

    conn.commit()


def fetch_forecast_accuracy(conn, city: str):
    cursor = conn.execute(
        """
        SELECT date, abs_error
        FROM forecast_accuracy
        WHERE city = ?
        ORDER BY date
        """,
        (city,),
    )

    return cursor.fetchall()
