import pandas as pd


def compute_mae(rows):
    if not rows:
        return None

    df = pd.DataFrame(rows, columns=["date", "abs_error"])
    return round(df["abs_error"].mean(), 2)


def prepare_accuracy_df(rows):
    """
    dataframe for accuracy trend visualization.
    """
    if not rows:
        return None

    df = pd.DataFrame(rows, columns=["date", "abs_error"])
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
    df = df.sort_values("date")

    # Rolling average to smooth noise (window = 3)
    df["rolling_mae"] = df["abs_error"].rolling(window=3).mean()

    return df
