from fastapi import FastAPI
from pydantic import BaseModel

import pandas as pd
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_absolute_percentage_error

app = FastAPI()

# =========================
# Request Body
# =========================

class ForecastRequest(BaseModel):
    sku_id: str
    forecast_days: int

# =========================
# Load Dataset
# =========================

df = pd.read_csv("demand_history.csv")

df['date'] = pd.to_datetime(df['date'])

# =========================
# Create Lag Features
# =========================

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

# =========================
# Forecast API
# =========================

@app.post("/api/forecast")

def forecast(req: ForecastRequest):

    sku_df = df[df['sku_id'] == req.sku_id]

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

    return {
        "sku_id": req.sku_id,
        "forecast_days": req.forecast_days,
        "predicted_demand": pred[:req.forecast_days].tolist(),
        "mape": round(mape, 2)
    }
