import pandas as pd
import plotly.graph_objects as go


def forecast_temperature_chart(df):
    """
    Accurate forecast visualization:
    - Avg temperature as main signal
    - Min–Max range as uncertainty band
    -  Hover tooltips show condition + rain probability
    -  No duplicate X-axis dates
    """

    df = df.copy()

    #  Fix duplicate tick labels
    df["date_label"] = pd.to_datetime(df["date"]).dt.strftime("%b %d")

    #  Ensure safe columns exist (for cached data too)
    if "condition" not in df.columns:
        df["condition"] = "N/A"
    if "rain_prob" not in df.columns:
        df["rain_prob"] = None

    #  Custom hover data bundle
    df["rain_prob_display"] = df["rain_prob"].apply(
        lambda x: f"{int(x)}%" if pd.notna(x) else "N/A"
    )

    fig = go.Figure()

    # --- Max Temp (Top Bound) ---
    fig.add_trace(
        go.Scatter(
            x=df["date_label"],
            y=df["max_temp"],
            mode="lines",
            line=dict(width=0),
            showlegend=False,
            hoverinfo="skip"
        )
    )

    # --- Min Temp (Bottom Bound) ---
    fig.add_trace(
        go.Scatter(
            x=df["date_label"],
            y=df["min_temp"],
            mode="lines",
            fill="tonexty",
            fillcolor="rgba(0, 180, 255, 0.15)",
            line=dict(width=0),
            name="Min–Max Range",
            hoverinfo="skip"
        )
    )

    # --- Avg Temp Line (Main Signal + Tooltip) ---
    fig.add_trace(
        go.Scatter(
            x=df["date_label"],
            y=df["avg_temp"],
            mode="lines+markers",
            name="Expected Avg Temperature (°C)",
            line=dict(color="#4FC3F7", width=3),
            marker=dict(size=7),

            #  Attach extra hover values
            customdata=list(zip(
                df["min_temp"],
                df["max_temp"],
                df["condition"],
                df["rain_prob_display"]
            )),

            #  Beautiful tooltip
            hovertemplate=(
                "<b>%{x}</b><br>"
                "🌡 Avg Temp: <b>%{y:.1f}°C</b><br>"
                "🔻 Min: %{customdata[0]:.1f}°C<br>"
                "🔺 Max: %{customdata[1]:.1f}°C<br>"
                "🌤 Condition: %{customdata[2]}<br>"
                "🌧 Rain Chance: %{customdata[3]}<br>"
                "<extra></extra>"
            )
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

    # category axis prevents duplicate date ticks
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
