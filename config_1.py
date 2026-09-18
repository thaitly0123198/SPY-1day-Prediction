from pathlib import Path

SNAPSHOT = Path("data/raw/spy_snapshot_2010-01-01_2026-08-31.csv")

LOOKBACK    = 60               # 60 trading days look back = 3 months/ can test different look back values later
TRAIN_START = "2010-03-31"     # the 61st trading day, we get the first Y (return) here

FOLDS = [                    
    {"name": 1, "train_end": "2020-12-31", "val_start": "2021-01-01", "val_end": "2021-12-31"},
    {"name": 2, "train_end": "2021-12-31", "val_start": "2022-01-01", "val_end": "2022-12-31"},
    {"name": 3, "train_end": "2022-12-31", "val_start": "2023-01-01", "val_end": "2023-12-31"},
]

TEST_START, TEST_END = "2024-01-01", "2026-08-28"   
FORECAST_ONLY_DATE = "2026-08-28"  # cant be used to fit the model, but can be used to check if the model is still valid for the most recent data                          

METRIC_PRIMARY, METRIC_SECONDARY = "MAE", "RMSE"    # percentage metrics
AGGREGATION = "mean of per-fold validation MAE"     # equal weight per year

SEEDS = {"gbdt": 42, "torch_dev": 0, "torch_report": [0, 1, 2]} 

GBDT_CONFIGS = [                                    # ← renamed from LGBM_CONFIGS
    {"name": "A", "max_depth": 3,       "eta": 0.05, "n_estimators": 200},
    {"name": "B", "max_depth": 6,       "eta": 0.05, "n_estimators": 300},
    {"name": "C", "max_depth": 3,       "eta": 0.03, "n_estimators": 400,
     "colsample_bytree": 0.8},
]
TORCH_CONFIGS = [                                   # unchanged
    {"name": "A", "hidden": [16, 8],  "lr": 1e-3, "weight_decay": 0.0,  "dropout": 0.0},
    {"name": "B", "hidden": [32, 16], "lr": 1e-3, "weight_decay": 1e-4, "dropout": 0.0},
    {"name": "C", "hidden": [16, 8],  "lr": 3e-4, "weight_decay": 1e-3, "dropout": 0.2},
]