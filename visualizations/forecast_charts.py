import plotly.express as px


def forecast_temperature_chart(df):
    """
    Plot forecast temperature trend (avg temp per day)
    """
    fig = px.line(
        df,
        x="date",
        y="avg_temp",
        title="5-Day Temperature Forecast (°C)",
        markers=True
    )

    fig.update_traces(
        line=dict(width=3, dash="dot")
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Date",
        yaxis_title="Avg Temperature (°C)"
    )

    return fig
