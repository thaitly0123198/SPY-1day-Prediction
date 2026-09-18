Training data set:
- records from 2010-01-01 to 2020-12-31

Evaluation data set:
- Evaluate in 3 folds (2021, 2022, 2023)
- Records rom 2021-01-01 to 2021-12-31 (first fold), 2022-01-01 to 2022-12-31 (second fold), 2023-01-01 to 2023-12-31 (third fold)

Test data set:
- Records from 2024-01-01 to 2026-08-28.

No dataset shuffling since its a timeseries dataset.

Data splits:
====================================================
scorable examples: 4128  (2010-03-31 -> 2026-08-27)
fold 1: train=2708  val=252  dropped_at_boundary=1
fold 2: train=2960  val=251  dropped_at_boundary=1
fold 3: train=3211  val=250  dropped_at_boundary=1
test (scored): 666  (2024-01-02 -> 2026-08-27)
  2024: 252
  2025: 250
  2026: 164