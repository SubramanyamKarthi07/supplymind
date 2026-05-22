import pandas as pd
from prophet import Prophet
import warnings

warnings.filterwarnings("ignore")

# =========================
# LOAD DATA
# =========================

df = pd.read_csv('demand_history.csv')

# Convert date column
df['date'] = pd.to_datetime(df['date'])

# =========================
# CHECK DEMAND COLUMN
# =========================

print("Columns in dataset:")
print(df.columns)

# Auto-detect demand column
possible_targets = [
    'quantity_demanded',
    'units_sold',
    'demand',
    'sales'
]

target_col = None

for col in possible_targets:
    if col in df.columns:
        target_col = col
        break

if target_col is None:
    raise Exception("No demand column found.")

print(f"\nUsing target column: {target_col}")

# =========================
# SELECT 5 SKUs
# =========================

test_skus = df['sku_id'].unique()[:5]

results = []

# =========================
# FORECAST LOOP
# =========================

for sku in test_skus:

    print("\n========================")
    print(f"Processing SKU: {sku}")
    print("========================")

    # Prepare data for Prophet
    sku_df = (
        df[df['sku_id'] == sku][['date', target_col]]
        .rename(columns={
            'date': 'ds',
            target_col: 'y'
        })
    )

    # Train-test split
    train = sku_df[sku_df['ds'] < '2024-01-01']
    test  = sku_df[sku_df['ds'] >= '2024-01-01']

    # Skip if insufficient data
    if len(train) < 30 or len(test) == 0:
        print("Not enough data.")
        continue

    # Create model
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False
    )

    # Train model
    model.fit(train)

    # Future dataframe
    future = model.make_future_dataframe(
        periods=len(test),
        freq='D'
    )

    # Forecast
    forecast = model.predict(future)

    # Predictions
    pred = forecast.tail(len(test))['yhat'].values
    actual = test['y'].values

    # Avoid divide-by-zero
    actual_safe = actual.copy()
    actual_safe[actual_safe == 0] = 1

    # MAPE Calculation
    mape = abs((actual - pred) / actual_safe).mean() * 100

    results.append({
        'sku_id': sku,
        'mape': round(mape, 2)
    })

    print(f"SKU {sku} — MAPE: {mape:.1f}%")

# =========================
# FINAL RESULTS
# =========================

print("\n========================")
print("FINAL RESULTS")
print("========================")

for r in results:
    print(f"SKU {r['sku_id']} -> MAPE: {r['mape']}%")

avg_mape = sum(r['mape'] for r in results) / len(results)

print(f"\nAverage MAPE: {avg_mape:.1f}%")
print("Target by Week 4: < 15%")

import pandas as pd
from prophet import Prophet
import warnings

warnings.filterwarnings("ignore")

# =========================
# LOAD DATA
# =========================

df = pd.read_csv('demand_history.csv')

# Convert date
df['date'] = pd.to_datetime(df['date'])

print("Dataset Columns:")
print(df.columns)

# =========================
# DETECT TARGET COLUMN
# =========================

possible_targets = [
    'quantity_demanded',
    'units_sold',
    'demand',
    'sales'
]

target_col = None

for col in possible_targets:
    if col in df.columns:
        target_col = col
        break

if target_col is None:
    raise Exception("No target demand column found.")

print(f"\nUsing target column: {target_col}")

# =========================
# CREATE FEATURES IF MISSING
# =========================

# Promotion feature
if 'is_promotion' not in df.columns:
    df['is_promotion'] = 0

# Weekend feature
if 'is_weekend' not in df.columns:
    df['is_weekend'] = df['date'].dt.dayofweek.isin([5,6]).astype(int)

# =========================
# SELECT TEST SKUS
# =========================

test_skus = df['sku_id'].unique()[:5]

results_v1 = []
results_v2 = []

# =========================
# LOOP THROUGH SKUS
# =========================

for sku in test_skus:

    print("\n===================================")
    print(f"Processing SKU: {sku}")
    print("===================================")

    # Prepare SKU dataframe
    sku_df = df[df['sku_id'] == sku][[
        'date',
        target_col,
        'is_promotion',
        'is_weekend'
    ]].rename(columns={
        'date': 'ds',
        target_col: 'y'
    })

    # Train/Test split
    train = sku_df[sku_df['ds'] < '2024-01-01']
    test  = sku_df[sku_df['ds'] >= '2024-01-01']

    # Skip insufficient data
    if len(train) < 30 or len(test) == 0:
        print("Not enough data.")
        continue

    # ===================================
    # V1 — BASIC PROPHET
    # ===================================

    m1 = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False
    )

    m1.fit(train[['ds', 'y']])

    future1 = m1.make_future_dataframe(
        periods=len(test),
        freq='D'
    )

    f1 = m1.predict(future1)

    p1 = f1.tail(len(test))['yhat'].values

    # ===================================
    # V2 — PROPHET WITH REGRESSORS
    # ===================================

    m2 = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False
    )

    m2.add_regressor('is_promotion')
    m2.add_regressor('is_weekend')

    m2.fit(train)

    future2 = m2.make_future_dataframe(
        periods=len(test),
        freq='D'
    )

    future2 = future2.merge(
        sku_df[['ds', 'is_promotion', 'is_weekend']],
        on='ds',
        how='left'
    ).fillna(0)

    f2 = m2.predict(future2)

    p2 = f2.tail(len(test))['yhat'].values

    # ===================================
    # CALCULATE MAPE
    # ===================================

    actual = test['y'].values

    actual_safe = actual.copy()
    actual_safe[actual_safe == 0] = 1

    mape1 = abs((actual - p1) / actual_safe).mean() * 100
    mape2 = abs((actual - p2) / actual_safe).mean() * 100

    results_v1.append(round(mape1, 2))
    results_v2.append(round(mape2, 2))

    print(f"SKU {sku}:")
    print(f"V1 MAPE = {mape1:.1f}%")
    print(f"V2 MAPE = {mape2:.1f}%")

# =========================
# FINAL RESULTS
# =========================

avg_v1 = sum(results_v1) / len(results_v1)
avg_v2 = sum(results_v2) / len(results_v2)

improvement = avg_v1 - avg_v2

print("\n===================================")
print("FINAL COMPARISON")
print("===================================")

print(f"Avg V1 MAPE: {avg_v1:.1f}%")
print(f"Avg V2 MAPE: {avg_v2:.1f}%")
print(f"Improvement: {improvement:.1f} percentage points")

if avg_v2 < avg_v1:
    print("\nYes — Adding regressors improved accuracy.")
else:
    print("\nNo significant improvement observed.")

import pandas as pd
from prophet import Prophet

df = pd.read_csv('demand_history.csv')
df['date'] = pd.to_datetime(df['date'])

# Add festive month flag
# Oct and Nov are festive season in India
df['is_festive'] = df['month'].isin(
    [10, 11]).astype(int)

test_skus = df['sku_id'].unique()[:5]
results = []

for sku in test_skus:
    sku_df = df[df['sku_id']==sku][[
        'date','quantity_demanded',
        'is_promotion','is_weekend',
        'is_festive'
    ]].rename(columns={
        'date':'ds',
        'quantity_demanded':'y'
    })

    train = sku_df[sku_df['ds'] < '2024-01-01']
    test  = sku_df[sku_df['ds'] >= '2024-01-01']

    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False,
        seasonality_mode='multiplicative'
    )
    model.add_regressor('is_promotion')
    model.add_regressor('is_weekend')
    model.add_regressor('is_festive')
    model.fit(train)

    future = model.make_future_dataframe(
        periods=len(test), freq='D')
    future = future.merge(
        sku_df[['ds','is_promotion',
                'is_weekend','is_festive']],
        on='ds', how='left').fillna(0)

    forecast = model.predict(future)
    pred = forecast.tail(len(test))['yhat'].values
    actual = test['y'].values
    mape = abs(
        (actual-pred)/actual.clip(1)
    ).mean()*100

    results.append({
        'sku_id': sku,
        'mape_v3': round(mape,2)
    })
    print(f"SKU {sku}: V3 MAPE = {mape:.1f}%")

avg = sum(r['mape_v3'] for r in results)/len(results)
print(f"\nAvg V3 MAPE: {avg:.1f}%")
print(f"V2 was: 55.5%")
print(f"Improvement: {55.5 - avg:.1f}pp")

Post V3 MAPE for all 5 SKUs.
Did festive season feature help?
Week 2 we add LightGBM on top of Prophet.

import pandas as pd
from prophet import Prophet
import warnings

warnings.filterwarnings("ignore")

# =====================================
# LOAD DATA
# =====================================

df = pd.read_csv('demand_history.csv')

# Convert date column
df['date'] = pd.to_datetime(df['date'])

print("Dataset Columns:")
print(df.columns)

# =====================================
# DETECT TARGET COLUMN
# =====================================

possible_targets = [
    'quantity_demanded',
    'units_sold',
    'demand',
    'sales'
]

target_col = None

for col in possible_targets:
    if col in df.columns:
        target_col = col
        break

if target_col is None:
    raise Exception("No target column found.")

print(f"\nUsing target column: {target_col}")

# =====================================
# DEFINE FESTIVE HOLIDAYS
# =====================================

festivities = pd.DataFrame({
    'holiday': 'festive_season',

    'ds': pd.to_datetime([
        '2023-10-01',
        '2023-11-30',
        '2024-10-01',
        '2024-11-30'
    ]),

    'lower_window': 0,
    'upper_window': 60,
})

print("\nFestive holidays configured.")

# =====================================
# SELECT 5 SKUs
# =====================================

test_skus = df['sku_id'].unique()[:5]

results = []

# =====================================
# LOOP THROUGH SKUs
# =====================================

for sku in test_skus:

    print("\n===================================")
    print(f"Processing SKU: {sku}")
    print("===================================")

    # Prepare SKU dataframe
    sku_df = (
        df[df['sku_id'] == sku][[
            'date',
            target_col
        ]]
        .rename(columns={
            'date': 'ds',
            target_col: 'y'
        })
    )

    # Train/Test split
    train = sku_df[sku_df['ds'] < '2024-01-01']
    test  = sku_df[sku_df['ds'] >= '2024-01-01']

    # Skip insufficient data
    if len(train) < 30 or len(test) == 0:
        print("Not enough data.")
        continue

    # =====================================
    # V2 — BASIC PROPHET
    # =====================================

    m2 = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False
    )

    m2.fit(train[['ds', 'y']])

    future2 = m2.make_future_dataframe(
        periods=len(test),
        freq='D'
    )

    f2 = m2.predict(future2)

    p2 = f2.tail(len(test))['yhat'].values

    # =====================================
    # V4 — HOLIDAY-BASED PROPHET
    # =====================================

    m4 = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False,
        holidays=festivities,
        seasonality_mode='multiplicative'
    )

    m4.fit(train[['ds', 'y']])

    future4 = m4.make_future_dataframe(
        periods=len(test),
        freq='D'
    )

    f4 = m4.predict(future4)

    p4 = f4.tail(len(test))['yhat'].values

    # =====================================
    # CALCULATE MAPE
    # =====================================

    actual = test['y'].values

    actual_safe = actual.copy()
    actual_safe[actual_safe == 0] = 1

    mape2 = abs(
        (actual - p2) / actual_safe
    ).mean() * 100

    mape4 = abs(
        (actual - p4) / actual_safe
    ).mean() * 100

    results.append({
        'sku_id': sku,
        'mape_v2': round(mape2, 2),
        'mape_v4': round(mape4, 2)
    })

    print(
        f"SKU {sku}: "
        f"V2={mape2:.1f}% → "
        f"V4={mape4:.1f}%"
    )

# =====================================
# FINAL RESULTS
# =====================================

avg2 = sum(r['mape_v2'] for r in results) / len(results)
avg4 = sum(r['mape_v4'] for r in results) / len(results)

improvement = avg2 - avg4

print("\n===================================")
print("FINAL COMPARISON")
print("===================================")

for r in results:
    print(
        f"SKU {r['sku_id']} -> "
        f"V2: {r['mape_v2']}% | "
        f"V4: {r['mape_v4']}%"
    )

print(f"\nAvg V2 MAPE: {avg2:.1f}%")
print(f"Avg V4 MAPE: {avg4:.1f}%")
print(f"Improvement: {improvement:.1f}pp")

if avg4 < avg2:
    print("\nYes — holidays approach improved MAPE.")
else:
    print("\nNo significant improvement observed.")

import pandas as pd
from prophet import Prophet

df = pd.read_csv('demand_history.csv')
df['date'] = pd.to_datetime(df['date'])

# Correct festive holidays
# Only the actual peak weeks
festivities = pd.DataFrame({
    'holiday': [
        'navratri_2023','diwali_2023',
        'navratri_2024','diwali_2024'
    ],
    'ds': pd.to_datetime([
        '2023-10-15',
        '2023-11-12',
        '2024-10-03',
        '2024-11-01'
    ]),
    'lower_window': [-7, -7, -7, -7],
    'upper_window': [7, 7, 7, 7],
})

test_skus = df['sku_id'].unique()[:5]
results = []

for sku in test_skus:
    sku_df = df[df['sku_id']==sku][[
        'date','quantity_demanded'
    ]].rename(columns={
        'date':'ds',
        'quantity_demanded':'y'
    })

    train = sku_df[sku_df['ds'] < '2024-01-01']
    test  = sku_df[sku_df['ds'] >= '2024-01-01']

    # V2 — no holidays baseline
    m2 = Prophet(yearly_seasonality=True,
                 weekly_seasonality=True,
                 daily_seasonality=False)
    m2.fit(train[['ds','y']])
    f2 = m2.predict(
        m2.make_future_dataframe(
            periods=len(test), freq='D'))
    p2 = f2.tail(len(test))['yhat'].values

    # V5 — correct narrow holiday windows
    m5 = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False,
        holidays=festivities
    )
    m5.fit(train[['ds','y']])
    f5 = m5.predict(
        m5.make_future_dataframe(
            periods=len(test), freq='D'))
    p5 = f5.tail(len(test))['yhat'].values

    actual = test['y'].values
    mape2 = abs(
        (actual-p2)/actual.clip(1)).mean()*100
    mape5 = abs(
        (actual-p5)/actual.clip(1)).mean()*100

    results.append({
        'sku_id': sku,
        'mape_v2': round(mape2,2),
        'mape_v5': round(mape5,2)
    })
    print(f"SKU {sku}: V2={mape2:.1f}% → V5={mape5:.1f}%")

avg2 = sum(r['mape_v2'] for r in results)/len(results)
avg5 = sum(r['mape_v5'] for r in results)/len(results)
print(f"\nAvg V2: {avg2:.1f}%")
print(f"Avg V5: {avg5:.1f}%")
print(f"Improvement: {avg2-avg5:.1f}pp")

import pandas as pd

# ============================
# LOAD DATA
# ============================

df = pd.read_csv('/demand_history.csv')

# Convert date column
df['date'] = pd.to_datetime(df['date'])

# Create month column
df['month'] = df['date'].dt.month

# ============================
# CHECK DEMAND COLUMN
# ============================

possible_targets = [
    'quantity_demanded',
    'units_sold',
    'demand',
    'sales'
]

target_col = None

for col in possible_targets:
    if col in df.columns:
        target_col = col
        break

if target_col is None:
    raise Exception("No demand column found.")

print(f"Using demand column: {target_col}")

# ============================
# MONTHLY DEMAND ANALYSIS
# ============================

monthly = (
    df.groupby('month')[target_col]
    .mean()
    .round(1)
)

print("\nAverage daily demand by month:")
print(monthly)

# ============================
# FESTIVE SPIKE ANALYSIS
# ============================

print("\nFestive spike (Oct-Nov vs rest):")

festive = monthly[[10, 11]].mean()

normal = monthly.drop([10, 11]).mean()

spike = festive / normal

print(f"Festive: {festive:.1f} units/day")
print(f"Normal: {normal:.1f} units/day")
print(f"Spike: {spike:.1f}x baseline")

!pip install lightgbm
import pandas as pd
import numpy as np
from prophet import Prophet
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_absolute_percentage_error
df = pd.read_csv('demand_history.csv')
df['date'] = pd.to_datetime(df['date'])
print(df.head())
test_skus = df['sku_id'].unique()[:3]
print(test_skus)
results = []
for sku in test_skus:

    print("\n================================")
    print(f"Processing {sku}")
    print("================================")

    # SKU data
    sku_df = df[df['sku_id'] == sku].copy()

    # Prophet format
    sku_df = sku_df.rename(columns={
        'date': 'ds',
        'quantity_demanded': 'y'
    })

    # Train/Test split
    train = sku_df[sku_df['ds'] < '2024-01-01']
    test  = sku_df[sku_df['ds'] >= '2024-01-01']

    # =====================================
    # STEP A — TRAIN PROPHET
    # =====================================

    prophet_model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False
    )

    prophet_model.fit(train[['ds', 'y']])

    # Prophet predictions for TRAIN
    train_future = train[['ds']]

    train_forecast = prophet_model.predict(train_future)

    train['prophet_pred'] = train_forecast['yhat'].values

    # =====================================
    # STEP B — CALCULATE RESIDUALS
    # =====================================

    train['residual'] = (
        train['y'] - train['prophet_pred']
    )

    # =====================================
    # STEP C — LIGHTGBM FEATURES
    # =====================================

    features = [
        'is_promotion',
        'month',
        'day_of_week'
    ]

    X_train = train[features]

    y_train = train['residual']

    # =====================================
    # STEP D — TRAIN LIGHTGBM
    # =====================================

    lgbm = LGBMRegressor()

    lgbm.fit(X_train, y_train)

    # =====================================
    # STEP E — PROPHET TEST PREDICTION
    # =====================================

    test_future = prophet_model.make_future_dataframe(
        periods=len(test),
        freq='D'
    )

    prophet_test_forecast = prophet_model.predict(
        test_future
    )

    prophet_pred_test = (
        prophet_test_forecast
        .tail(len(test))['yhat']
        .values
    )

    # =====================================
    # STEP F — LIGHTGBM CORRECTION
    # =====================================

    X_test = test[features]

    lgbm_correction = lgbm.predict(X_test)

    # =====================================
    # STEP G — FINAL HYBRID FORECAST
    # =====================================

    final_pred = (
        prophet_pred_test + lgbm_correction
    )

    # =====================================
    # STEP H — CALCULATE MAPE
    # =====================================

    actual = test['y'].values

    hybrid_mape = (
        mean_absolute_percentage_error(
            actual,
            final_pred
        ) * 100
    )

    prophet_mape = (
        mean_absolute_percentage_error(
            actual,
            prophet_pred_test
        ) * 100
    )

    print(f"Prophet MAPE: {prophet_mape:.2f}%")
    print(f"Hybrid MAPE : {hybrid_mape:.2f}%")

    results.append({
        'sku': sku,
        'prophet_mape': round(prophet_mape, 2),
        'hybrid_mape': round(hybrid_mape, 2)
    })
    print("\n========== FINAL RESULTS ==========")

for r in results:

    print(
        f"{r['sku']} | "
        f"Prophet: {r['prophet_mape']}% | "
        f"Hybrid: {r['hybrid_mape']}%"
    )
    !pip install lightgbm
    import pandas as pd
import numpy as np

from lightgbm import LGBMRegressor

from sklearn.metrics import mean_absolute_percentage_error
df = pd.read_csv('/content/intenship/demand_history.csv')

df['date'] = pd.to_datetime(df['date'])

print(df.head())
df['lag_7'] = df.groupby('sku_id')[
    'quantity_demanded'
].shift(7)

df['lag_14'] = df.groupby('sku_id')[
    'quantity_demanded'
].shift(14)

df['lag_28'] = df.groupby('sku_id')[
    'quantity_demanded'
].shift(28)

df['rolling_7'] = df.groupby('sku_id')[
    'quantity_demanded'
].transform(
    lambda x: x.shift(1).rolling(7).mean()
)

df['rolling_28'] = df.groupby('sku_id')[
    'quantity_demanded'
].transform(
    lambda x: x.shift(1).rolling(28).mean()
)

print("Lag features created")
df = df.dropna()

print(df.shape)
test_skus = df['sku_id'].unique()[:5]

print(test_skus)
for sku in test_skus:

    print("\n==========================")
    print(f"Processing {sku}")
    print("==========================")

    sku_df = df[df['sku_id'] == sku].copy()

    # Train/Test split
    train = sku_df[
        sku_df['date'] < '2024-01-01'
    ]

    test = sku_df[
        sku_df['date'] >= '2024-01-01'
    ]

    # Features
    features = [
        'lag_7',
        'lag_14',
        'lag_28',
        'rolling_7',
        'rolling_28',
        'month',
        'is_promotion'
    ]

    X_train = train[features]
    y_train = train['quantity_demanded']

    X_test = test[features]
    y_test = test['quantity_demanded']

    # Train LightGBM
    model = LGBMRegressor()

    model.fit(X_train, y_train)

    # Predict
    pred = model.predict(X_test)

    # MAPE
    mape = (
        mean_absolute_percentage_error(
            y_test,
            pred
        ) * 100
    )

    print(f"LightGBM MAPE: {mape:.2f}%")

    results.append({
        'sku': sku,
        'lgbm_mape': round(mape, 2)
    })
    print("\n========== FINAL RESULTS ==========")

for r in results:

    print(
        f"{r['sku']} | "
        f"LightGBM MAPE: "
        f"{r['lgbm_mape']}%"
    )
    from google.colab import drive
drive.mount('/content/drive')
import pandas as pd
import numpy as np

from prophet import Prophet
from lightgbm import LGBMRegressor

from sklearn.metrics import mean_absolute_percentage_error
path = "/content/drive/MyDrive/Internship /demand_history.csv"

df = pd.read_csv(path)

df['date'] = pd.to_datetime(df['date'])

print(df.head())
df['lag_7'] = df.groupby('sku_id')[
    'quantity_demanded'
].shift(7)

df['lag_14'] = df.groupby('sku_id')[
    'quantity_demanded'
].shift(14)

df['lag_28'] = df.groupby('sku_id')[
    'quantity_demanded'
].shift(28)

df['rolling_7'] = df.groupby('sku_id')[
    'quantity_demanded'
].transform(
    lambda x: x.shift(1).rolling(7).mean()
)

df['rolling_28'] = df.groupby('sku_id')[
    'quantity_demanded'
].transform(
    lambda x: x.shift(1).rolling(28).mean()
)

df = df.dropna()

print("Lag features created")
top_50_skus = df['sku_id'].unique()[:50]

print(len(top_50_skus))
lgb_mapes = []

for sku in top_50_skus:

    sku_df = df[df['sku_id'] == sku]

    train = sku_df[
        sku_df['date'] < '2024-01-01'
    ]

    test = sku_df[
        sku_df['date'] >= '2024-01-01'
    ]

    features = [
        'lag_7',
        'lag_14',
        'lag_28',
        'rolling_7',
        'rolling_28',
        'month',
        'is_promotion'
    ]

    X_train = train[features]
    y_train = train['quantity_demanded']

    X_test = test[features]
    y_test = test['quantity_demanded']

    model = LGBMRegressor()

    model.fit(X_train, y_train)

    pred = model.predict(X_test)

    mape = (
        mean_absolute_percentage_error(
            y_test,
            pred
        ) * 100
    )

    lgb_mapes.append(mape)

print("Standalone avg:",
      np.mean(lgb_mapes))

print("Standalone std:",
      np.std(lgb_mapes))
hybrid_mapes = []

for sku in top_50_skus:

    sku_df = df[df['sku_id'] == sku].copy()

    prophet_df = sku_df.rename(columns={
        'date': 'ds',
        'quantity_demanded': 'y'
    })

    train = prophet_df[
        prophet_df['ds'] < '2024-01-01'
    ]

    test = prophet_df[
        prophet_df['ds'] >= '2024-01-01'
    ]

    # =========================
    # PROPHET MODEL
    # =========================

    prophet_model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False
    )

    prophet_model.fit(train[['ds', 'y']])

    future = prophet_model.make_future_dataframe(
        periods=len(test),
        freq='D'
    )

    forecast = prophet_model.predict(future)

    prophet_pred = (
        forecast.tail(len(test))['yhat']
        .values
    )

    # =========================
    # RESIDUALS
    # =========================

    train_future = train[['ds']]

    train_forecast = prophet_model.predict(
        train_future
    )

    train['prophet_pred'] = (
        train_forecast['yhat'].values
    )

    train['residual'] = (
        train['y'] -
        train['prophet_pred']
    )

    # =========================
    # LIGHTGBM ON RESIDUALS
    # =========================

    features = [
        'lag_7',
        'lag_14',
        'lag_28',
        'rolling_7',
        'rolling_28',
        'month',
        'is_promotion'
    ]

    X_train = train[features]

    y_train = train['residual']

    X_test = test[features]

    lgbm = LGBMRegressor()

    lgbm.fit(X_train, y_train)

    residual_pred = lgbm.predict(X_test)

    # =========================
    # FINAL HYBRID FORECAST
    # =========================

    final_pred = (
        prophet_pred +
        residual_pred
    )

    actual = test['y'].values

    hybrid_mape = (
        mean_absolute_percentage_error(
            actual,
            final_pred
        ) * 100
    )

    hybrid_mapes.append(hybrid_mape)

print("Hybrid avg:",
      np.mean(hybrid_mapes))

print("Hybrid std:",
      np.std(hybrid_mapes))
print("\n========== FINAL RESULTS ==========")

print(f"\nStandalone LightGBM Avg MAPE : {lgb_avg:.2f}%")
print(f"Standalone LightGBM Std Dev : {lgb_std:.2f}")

print(f"\nHybrid Avg MAPE : {hybrid_avg:.2f}%")
print(f"Hybrid Std Dev : {hybrid_std:.2f}")

print("\nArchitecture Decision:")

if lgb_avg < hybrid_avg and lgb_std < hybrid_std:
    print("Standalone LightGBM selected")
else:
    print("Hybrid Prophet + LightGBM selected")
    lgb_avg = np.mean(lgb_mapes)
hybrid_avg = np.mean(hybrid_mapes)
import numpy as np

lgb_avg = np.mean(lgb_mapes)
lgb_std = np.std(lgb_mapes)

hybrid_avg = np.mean(hybrid_mapes)
hybrid_std = np.std(hybrid_mapes)
print("\n========== FINAL RESULTS ==========")

print(f"\nStandalone LightGBM Avg MAPE : {lgb_avg:.2f}%")
print(f"Standalone LightGBM Std Dev : {lgb_std:.2f}")

print(f"\nHybrid Avg MAPE : {hybrid_avg:.2f}%")
print(f"Hybrid Std Dev : {hybrid_std:.2f}")

print("\nArchitecture Decision:")

if lgb_avg < hybrid_avg and lgb_std < hybrid_std:
    print("Standalone LightGBM selected")
else:
    print("Hybrid Prophet + LightGBM selected")
