import plotly.express as px


def accuracy_trend_chart(df):
    """
    Plot forecast error over time.
    """

    fig = px.line(
        df,
        x="date",
        y="abs_error",
        markers=True,
        title="Forecast Accuracy Trend (Absolute Error °C)",
        labels={
            "abs_error": "Absolute Error (°C)",
            "date": "Date"
        }
    )

    #  FORCE categorical axis (NO timestamps)
    fig.update_xaxes(type="category")

    # Rolling MAE overlay (drop NaNs to prevent axis re-inference)
    if "rolling_mae" in df.columns:
        clean_df = df.dropna(subset=["rolling_mae"])

        fig.add_scatter(
            x=clean_df["date"],
            y=clean_df["rolling_mae"],
            mode="lines",
            name="Rolling MAE",
            line=dict(dash="dash")
        )

    fig.update_layout(template="plotly_white")
    return fig
