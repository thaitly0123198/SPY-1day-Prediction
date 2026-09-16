import yfinance as yf
import pandas as pd
import sys
from pathlib import Path

TICKER = "SPY"
START_DATE = "2010-01-01"
END_DATE = "2026-08-31"

def download_data(ticker, start_date, end_date) -> pd.DataFrame:
    data = yf.download(ticker, start=start_date, end=end_date, interval='1d', auto_adjust=False, keepna=True, actions=True)
    if data.empty:
        sys.exit(f"Download failed for ticker '{ticker}' between {start_date} and {end_date}.")

    data.columns = data.columns.get_level_values(0) # remove 'SPY' column level
    data.index = pd.to_datetime(data.index.date) # convert index to datetime.date
    data.columns = [c.lower().replace(" ", "_") for c in data.columns] 

    return data

def validate_download_data(data: pd.DataFrame) ->bool:
    if data.empty:
        print("Data validation failed: DataFrame is empty.")
        return False
    if not all(col in data.columns for col in ["open", "high", "low", "capital_gains", "stock_splits", "close", "adj_close", "volume"]):
        print("Data validation failed: Missing required columns.")
        return False
    if data.isnull().values.any():
        print("Data validation failed: DataFrame contains NaN values.")
        return False
    return True

def main():
    RAW_DIR = Path("data/raw")
    SNAPSHOT = RAW_DIR / f"spy_snapchot_{START_DATE}_{END_DATE}.csv"
    
    data = download_data(TICKER, START_DATE, END_DATE)
    valid = validate_download_data(data)
    if not valid:
        sys.exit("Data validation failed!")

    data.to_csv(SNAPSHOT)  
    print(data)


if __name__ == "__main__":
    main()