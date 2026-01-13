import pandas as pd
import plotly.graph_objects as go


def forecast_temperature_chart(df):
    """
    Accurate 5-day forecast visualization:
    - Avg temperature as main signal
    - Min-Max range as uncertainty band
    - Fix duplicate dates on x-axis by forcing date-only + category axis
    """

    df = df.copy()

    # Fix duplicate tick labels (remove time part completely)
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%b %d")

    fig = go.Figure()

    # --- Min-Max Range (Uncertainty Band) ---
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["max_temp"],
            mode="lines",
            line=dict(width=0),
            showlegend=False,
            hoverinfo="skip"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["min_temp"],
            mode="lines",
            fill="tonexty",
            fillcolor="rgba(0, 180, 255, 0.15)",
            line=dict(width=0),
            name="Min–Max Range"
        )
    )

    # --- Average Temperature Line ---
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["avg_temp"],
            mode="lines+markers",
            name="Expected Avg Temperature (°C)",
            line=dict(color="#4FC3F7", width=3),
            marker=dict(size=7)
        )
    )

    # --- Layout ---
    fig.update_layout(
        title="5-Day Temperature Forecast (Expected Value with Range)",
        xaxis_title="Date",
        yaxis_title="Temperature (°C)",
        template="plotly_dark",
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    # Force category axis (prevents Plotly from duplicating datetime ticks)
    fig.update_xaxes(
        type="category",
        showgrid=False
    )

    fig.update_yaxes(
        zeroline=True,
        zerolinewidth=1,
        zerolinecolor="rgba(255,255,255,0.2)"
    )

    return fig
