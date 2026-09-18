import pandas as pd
from config_1 import (SNAPSHOT, FOLDS, TRAIN_START, TEST_START,
                        TEST_END, LOOKBACK)

df = pd.read_csv(SNAPSHOT, index_col=0, parse_dates=True)
ex = pd.DataFrame({"issue": df.index[LOOKBACK:-1], "target": df.index[LOOKBACK + 1:]})
print(f"scorable examples: {len(ex)}  "
      f"({ex.issue.iloc[0].date()} -> {ex.issue.iloc[-1].date()})")

for f in FOLDS:
    issued = ex[(ex.issue >= TRAIN_START) & (ex.issue <= f["train_end"])]
    tr = issued[issued.target <= f["train_end"]]          # boundary rule
    va = ex[(ex.issue >= f["val_start"]) & (ex.issue <= f["val_end"])]
    dropped = len(issued) - len(tr)
    print(f"fold {f['name']}: train={len(tr):4d}  val={len(va):3d}  "
          f"dropped_at_boundary={dropped}")

te = ex[(ex.issue >= TEST_START) & (ex.issue <= TEST_END)]
print(f"test (scored): {len(te)}  ({te.issue.iloc[0].date()} -> {te.issue.iloc[-1].date()})")
for yr in (2024, 2025, 2026):
    print(f"  {yr}: {len(te[te.issue.dt.year == yr])}")

# scorable examples: 4128  (2010-03-31 -> 2026-08-27)
# fold 1: train=2708  val=252  dropped_at_boundary=1
# fold 2: train=2960  val=251  dropped_at_boundary=1
# fold 3: train=3211  val=250  dropped_at_boundary=1
# test (scored): 666  (2024-01-02 -> 2026-08-27)
#   2024: 252
#   2025: 250
#   2026: 164