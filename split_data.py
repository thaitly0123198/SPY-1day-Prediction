import json
from pathlib import Path

import numpy as np
import pandas as pd

from config_1 import LOOKBACK, SNAPSHOT, TEST_START, FORECAST_ONLY_DATE

PROCESS_DATA_DIR = Path("data/processed")

# calculate returns aka percentage changes from closing price of 1 trading day to the previous
# row 0 has no prior close so it'll be NaN, cut out later
def get_investment_returns(df: pd.DataFrame) -> pd.DataFrame:
    return df["adj_close"].pct_change() * 100

# get lookback window data (60 previous inv. returns, including the return from 
# the day the prediction is made / NOT the day the prediction is about, that is Y)
# 'position' start at the 60th row
def get_xRows_before_position_i(returns: pd.Series, position: int) -> np.ndarray:
    oldest = position - LOOKBACK + 1
    newest_exclusive = position + 1
    return returns.iloc[oldest:newest_exclusive].to_numpy()

def prep_model_ready_data(df: pd.DataFrame) -> pd.DataFrame:
    returns = get_investment_returns(df)
    trading_days = df.index

    # forecast_on_dates is the day the forecast/prediction is ON
    # target_dates is the day the forecast/prediction is ABOUT
    X_rows, forecast_on_dates, target_dates, ys = [], [], [], []

    for position in range(LOOKBACK, len(df) - 1):
        X_rows.append(get_xRows_before_position_i(returns, position))
        forecast_on_dates.append(trading_days[position])      # the guess is made on this date
        target_dates.append(trading_days[position + 1])    # the answer lands on this date
        ys.append(returns.iloc[position + 1])          # the actual return on the trading_days[position + 1]

    model_ready_data = pd.DataFrame(np.array(X_rows), columns=[f"x{i}" for i in range(LOOKBACK)])
    model_ready_data["forecast_date"] = forecast_on_dates
    model_ready_data["target_date"] = target_dates
    model_ready_data["y"] = ys
    return model_ready_data

def split_data(model_ready_df:  pd.DataFrame):
    date = model_ready_df["forecast_date"]

    training_data = model_ready_df[date < TEST_START]
    test_data = model_ready_df[(date >= TEST_START) & (date < FORECAST_ONLY_DATE)]

    return training_data, test_data

def main():
    PROCESS_DATA_DIR.mkdir(parents=True, exist_ok=True)
    data = pd.read_csv(SNAPSHOT, index_col=0, parse_dates=True)

    examples = prep_model_ready_data(data)

    # Boundary sanity — the dates M4 verified. If LOOKBACK or the snapshot
    # ever changes, this fires here, before anything downstream trusts it.
    first = examples.iloc[0]
    assert first["forecast_date"] == pd.Timestamp("2010-03-31")
    assert first["target_date"] == pd.Timestamp("2010-04-01")

    training_data, test_data = split_data(examples)

    # use parquet to keep dtypes and gives accurate floating points without conversion
    training_data.to_parquet(PROCESS_DATA_DIR / "training_data.parquet", index=False)
    test_data.to_parquet(PROCESS_DATA_DIR / "test_data.parquet", index=False)

if __name__ == "__main__":
    main()

