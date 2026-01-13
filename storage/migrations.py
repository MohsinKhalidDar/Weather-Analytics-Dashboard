import sqlite3

def get_table_columns(conn: sqlite3.Connection, table_name: str) -> set:
    cursor = conn.execute(f"PRAGMA table_info({table_name});")
    return {row[1] for row in cursor.fetchall()}  # row[1] = column name


def add_column_if_missing(conn: sqlite3.Connection, table: str, column: str, col_type: str):
    cols = get_table_columns(conn, table)

    if column not in cols:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_type};")
        conn.commit()


def run_migrations(conn: sqlite3.Connection):
    """
    Run all schema migrations safely (non-destructive).
    """

    #  Migration: add missing columns in weather_forecast table
    add_column_if_missing(conn, "weather_forecast", "icon", "TEXT")
    add_column_if_missing(conn, "weather_forecast", "rain_prob", "INTEGER")

     
