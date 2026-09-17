import yfinance as yf
import pandas as pd
import sys
import json
from datetime import datetime, timezone
from pathlib import Path

EXPECTED_COLUMNS = ["open", "high", "low", "dividends", "capital_gains", "stock_splits", "close", "adj_close", "volume"]

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
    if not all(col in data.columns for col in EXPECTED_COLUMNS):
        print("Data validation failed: Missing required columns.")
        return False
    if data.isnull().values.any():
        print("Data validation failed: DataFrame contains NaN values.")
        return False
    return True

def main():
    TICKER = "SPY"
    START_DATE = "2010-01-01"
    END_DATE = "2026-08-31"
    RAW_DIR = Path("data/raw")
    SNAPSHOT = RAW_DIR / f"spy_snapshot_{START_DATE}_{END_DATE}.csv"
    
    data = download_data(TICKER, START_DATE, END_DATE)
    valid = validate_download_data(data)
    div = data["dividends"].copy()
    spl = data["stock_splits"].copy()
    if not valid:
        sys.exit("Data validation failed!")



    data.to_csv(SNAPSHOT)  
    manifest = {
        "ticker": TICKER,
        "provider": "Yahoo Finance via yfinance",
        "downloaded_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "requested": {"start": START_DATE, "end_exclusive": END_DATE,
                      "interval": "1d", "auto_adjust": False},
        "normalization": ["flattened MultiIndex columns",
                          "index -> naive dates", "column names lowercased"],
        "library_versions": {"yfinance": yf.__version__, "pandas": pd.__version__,
                             "python": sys.version.split()[0]},
        "snapshot": {"filename": SNAPSHOT.name, 
                     "rows": len(data), "columns": list(data.columns),
                     "first_session": str(data.index[0].date()),
                     "last_session": str(data.index[-1].date())},
        "corporate_actions": {"dividends_rows": len(div), "splits_rows": len(spl)}
    }
    (RAW_DIR / "data_manifest.json").write_text(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()