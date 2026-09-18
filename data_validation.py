import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import pandas_market_calendars as mcal
from pathlib import Path

RAW_DIR = Path("data/raw")
START_DATE = "2010-01-01"
END_DATE = "2026-08-31"
EXPECTED_COLUMNS = ["open", "high", "low", "dividends", "capital_gains", "stock_splits", "close", "adj_close", "volume"]
SNAPSHOT = RAW_DIR / f"spy_snapshot_{START_DATE}_{END_DATE}.csv"
df = pd.read_csv(SNAPSHOT, index_col=0, parse_dates=True)


def get_columns_types(df: pd.DataFrame):
    columns_types = {}
    for col in df.columns:
        columns_types[col] = str(df[col].dtype)
    return columns_types

# check for invalid values (<= 0) for all columns except "dividends", "capital_gains", and "stock_splits"
def get_invalid_vals_count(df: pd.DataFrame) -> int:
    invalid_vals_count = 0

    for col in EXPECTED_COLUMNS:
        if col not in ["dividends", "capital_gains", "stock_splits"]:
            invalid_values = (df[col] <= 0).sum()
            if invalid_values > 0:
                invalid_vals_count += 1
    return invalid_vals_count

def get_missing_dates_info(df: pd.DataFrame):
    # identify missing trading days, check if they matches the closed trading days 
    # (weekends, holidays) and if there are any unexpected gaps in the data.
    missing_week_days = dict()
    complete_range = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')
    missing_dates = complete_range.difference(df.index)

    # Identify missing dates and count them by day of the week
    for date in missing_dates:
        if date.strftime('%a') in missing_week_days:
            missing_week_days[date.strftime('%a')] += 1
        else:
            missing_week_days[date.strftime('%a')] = 1

    # CHeck if the missing dates are valid market holidays or weekends
    nyse = mcal.get_calendar("NYSE")
    market_open_days = nyse.valid_days(start_date=START_DATE, end_date=END_DATE) # Load the NYSE calendar (works for major US equities)
    invalid_missing_dates_count = 0
    for date in missing_dates:
        if date.tz_localize('UTC') in market_open_days:
            invalid_missing_dates_count += 1
    return missing_dates, missing_week_days, invalid_missing_dates_count


def main():
    df = pd.read_csv(SNAPSHOT, index_col=0, parse_dates=True)

    # check data types
    columns_types = get_columns_types(df)

    # row duplicates check
    duplicate_rows_count = df.duplicated().sum()

    # missing values check
    NaN_vals_count = df.isna().sum().sum()

    # invalid values check
    invalid_vals_count = get_invalid_vals_count(df)

    # missing dates check
    missing_dates, missing_week_days_counts, invalid_missing_dates_count = get_missing_dates_info(df)

    data_validation_info = {
        "data_snapshot":    str(SNAPSHOT),
        "requested": {"start": START_DATE, "end_exclusive": END_DATE,
                        "interval": "1d"},
        "columns_types":  {
            "columns_types": columns_types,
            "is_all_numeric": all(dtype in ["float64", "int64"] for dtype in columns_types.values())
        },
        "duplicate_rows": {
            "count": int(duplicate_rows_count),
            "has_duplicates": bool(duplicate_rows_count > 0)
        },
        "timeseries_missing_values": {
            "count": int(NaN_vals_count),
            "has_missing_values": bool(NaN_vals_count > 0)
        },
        "invalid_values": {
            "count": int(invalid_vals_count),
            "has_invalid_values": bool(invalid_vals_count > 0)
        },
        "missing_dates": {
            "count": len(missing_dates),
            "has_missing_dates": bool(len(missing_dates) > 0),
            "missing_dates": [str(date.date()) for date in missing_dates]
        },
        "missing_dates_by_weekday": {
            "missing_week_days": {day: int(count) for day, count in missing_week_days_counts.items()},
            "missing_days_on_valid_market_days": bool(invalid_missing_dates_count > 0)
        },
        "summary": {
            "is_valid": all(
                [
                    all(dtype in ["float64", "int64"] for dtype in columns_types.values()),
                    duplicate_rows_count == 0,
                    NaN_vals_count == 0,
                    invalid_vals_count == 0,
                    len(missing_dates) != 0, #market always has closed days
                    invalid_missing_dates_count == 0
                ]
            )
        }
    }
    (RAW_DIR / "data_validation_info1.json").write_text(json.dumps(data_validation_info, indent=2))
if __name__ == "__main__":
    main()