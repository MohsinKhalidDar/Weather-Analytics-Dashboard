import pandas as pd
import plotly.express as px


def temp_comparison_chart(features: dict):
    df = pd.DataFrame({
        "Metric": ["Temperature", "Feels Like"],
        "Value": [features["temperature"], features["feels_like"]]
    })

    fig = px.bar(
        df,
        x="Metric",
        y="Value",
        title="Temperature vs Feels Like (°C)",
        text="Value"
    )
    fig.update_layout(template="plotly_white")
    return fig


def radar_weather_chart(features: dict):
    df = pd.DataFrame({
        "Metric": ["Temperature", "Humidity", "Wind", "Pressure"],
        "Value": [
            features["temperature"],
            features["humidity"],
            features["wind_speed"],
            features["pressure"] / 10
        ]
    })

    fig = px.line_polar(
        df,
        r="Value",
        theta="Metric",
        line_close=True,
        title="Weather Balance Radar"
    )
    fig.update_traces(fill="toself")
    fig.update_layout(template="plotly_white")
    return fig


def historical_trend_charts(rows):
    if rows is None or len(rows) < 2:
        return None, None

    df = pd.DataFrame(
        rows,
        columns=["timestamp", "temperature", "health"]
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    temp_fig = px.line(
        df,
        x="timestamp",
        y="temperature",
        title="Historical Temperature Trend (°C)",
        markers=True
    )
    temp_fig.update_traces(line=dict(width=3))
    temp_fig.update_layout(template="plotly_white")

    health_fig = px.line(
        df,
        x="timestamp",
        y="health",
        title="Historical Health Score Trend",
        markers=True
    )
    health_fig.update_traces(line=dict(width=3))
    health_fig.update_layout(template="plotly_white")

    return temp_fig, health_fig
