import plotly.graph_objects as go


def forecast_temperature_chart(df):
    fig = go.Figure()

    # Min–Max shaded band
    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["max_temp"],
        line=dict(color="rgba(135,206,250,0.2)"),
        showlegend=False,
        hoverinfo="skip"
    ))

    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["min_temp"],
        fill="tonexty",
        fillcolor="rgba(135,206,250,0.25)",
        line=dict(color="rgba(135,206,250,0.2)"),
        name="Min–Max Range"
    ))

    # Daytime (max temp) line
    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["max_temp"],
        mode="lines+markers",
        line=dict(color="#4FC3F7", width=3),
        marker=dict(size=8),
        name="Daytime Temperature (°C)"
    ))

    fig.update_layout(
        title="5-Day Temperature Forecast (Daytime with Range)",
        xaxis_title="Date",
        yaxis_title="Temperature (°C)",
        template="plotly_dark",
        hovermode="x unified"
    )

    return fig
