import pandas as pd
import numpy as np
import math
from sqlalchemy import create_engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import date, timedelta
import uvicorn
import nest_asyncio

# Fix async issue
nest_asyncio.apply()

# PostgreSQL connection
engine = create_engine(
    'postgresql://YOUR_USERNAME:YOUR_PASSWORD@localhost:5432/postgres'
)

# FastAPI app
app = FastAPI(title="SupplyMind Analytics API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# KPI Cache
cached_kpis = {}

def compute_dashboard_kpis():
    global cached_kpis

    # Inventory KPIs
    inv = pd.read_sql("""
        SELECT
            COUNT(DISTINCT sku_id) as total_skus,
            SUM(CASE WHEN days_of_cover < 7
                THEN 1 ELSE 0 END) as critical,
            SUM(CASE WHEN days_of_cover
                BETWEEN 7 AND 14
                THEN 1 ELSE 0 END) as warning,
            ROUND(AVG(days_of_cover)::numeric,1)
                as avg_doc
        FROM inventory_positions
        WHERE date = (
            SELECT MAX(date)
            FROM inventory_positions
        )
    """, engine).to_dict(orient='records')[0]

    # Supplier KPIs
    sup = pd.read_sql("""
        SELECT
            ROUND(AVG(otif_percentage)::numeric,2)
                as avg_otif,
            COUNT(DISTINCT CASE
                WHEN otif_percentage < 75
                THEN supplier_id END)
                as high_risk_count,
            COUNT(DISTINCT supplier_id)
                as total_suppliers
        FROM supplier_performance
        WHERE month = (
            SELECT MAX(month)
            FROM supplier_performance
        )
    """, engine).to_dict(orient='records')[0]

    # Store in cache
    cached_kpis = {
        'total_skus': inv['total_skus'],
        'critical_alerts': inv['critical'],
        'warning_alerts': inv['warning'],
        'avg_days_of_cover': inv['avg_doc'],
        'avg_otif': sup['avg_otif'],
        'high_risk_suppliers': sup['high_risk_count'],
        'total_suppliers': sup['total_suppliers']
    }

    print("KPIs refreshed successfully")

compute_dashboard_kpis()
scheduler = BackgroundScheduler()
scheduler.add_job(compute_dashboard_kpis, 'interval', hours=24)
scheduler.start()


@app.get("/api/analytics/inventory-health")
def inventory_health():

    query = """
    SELECT
        COUNT(DISTINCT sku_id) as total_skus,
        SUM(CASE WHEN days_of_cover < 7
            THEN 1 ELSE 0 END) as critical,
        SUM(CASE WHEN days_of_cover
            BETWEEN 7 AND 14
            THEN 1 ELSE 0 END) as warning,
        SUM(CASE WHEN days_of_cover > 60
            THEN 1 ELSE 0 END) as overstock,
        ROUND(AVG(days_of_cover)::numeric,1)
            as avg_doc
    FROM inventory_positions
    WHERE date = (
        SELECT MAX(date)
        FROM inventory_positions
    )
    """

    result = pd.read_sql(query, engine)

    return result.to_dict(orient='records')[0]


@app.get("/api/analytics/reorder-alerts")
def reorder_alerts():

    query = """
    SELECT
        sk.sku_name,
        sk.category,
        ip.closing_stock_units,
        sk.reorder_point_units,
        ip.days_of_cover,
        CASE
            WHEN ip.days_of_cover < 7
            THEN 'Critical'
            WHEN ip.days_of_cover < 14
            THEN 'Warning'
            ELSE 'OK'
        END as urgency
    FROM skus sk
    JOIN inventory_positions ip
        ON sk.sku_id = ip.sku_id
    WHERE ip.date = (
        SELECT MAX(date)
        FROM inventory_positions
    )
    AND ip.is_low_stock_alert = 1
    ORDER BY ip.days_of_cover ASC
    LIMIT 20
    """

    result = pd.read_sql(query, engine)

    return result.to_dict(orient='records')


@app.get("/api/analytics/supplier-summary")
def supplier_summary():

    query = """
    SELECT
        ROUND(AVG(otif_percentage)::numeric,2)
            as avg_otif,
        COUNT(DISTINCT CASE
            WHEN otif_percentage < 75
            THEN supplier_id END)
            as high_risk_count,
        COUNT(DISTINCT supplier_id)
            as total_suppliers
    FROM supplier_performance
    WHERE month = (
        SELECT MAX(month)
        FROM supplier_performance
    )
    """

    result = pd.read_sql(query, engine)

    return result.to_dict(orient='records')[0]


@app.get("/api/analytics/demand-accuracy")
def demand_accuracy():

    query = """
    SELECT
        sk.category,
        COUNT(DISTINCT dh.sku_id) as sku_count,
        ROUND(AVG(dh.quantity_demanded)::numeric,1)
            as avg_daily_demand,
        SUM(CASE WHEN dh.is_promotion = 1
            THEN 1 ELSE 0 END) as promotion_days,
        SUM(CASE WHEN dh.month IN (10,11)
            THEN dh.quantity_demanded
            ELSE 0 END) as festive_demand,
        SUM(CASE WHEN dh.month NOT IN (10,11)
            THEN dh.quantity_demanded
            ELSE 0 END) as normal_demand
    FROM demand_history dh
    JOIN skus sk
        ON dh.sku_id = sk.sku_id
    WHERE dh.date >= '2024-01-01'
    GROUP BY sk.category
    ORDER BY avg_daily_demand DESC
    """

    result = pd.read_sql(query, engine)

    return result.to_dict(orient='records')


@app.get("/api/analytics/dashboard-summary")
def dashboard_summary():

    return cached_kpis


@app.get("/api/analytics/refresh")
def refresh_dashboard():

    compute_dashboard_kpis()

    return {
        "status": "success",
        "message": "KPI cache refreshed",
        "cached_kpis": cached_kpis
    }


@app.get("/health")
def health():

    return {
        "status": "ok",
        "service": "SupplyMind Analytics API"
    }


@app.get("/api/analytics/disruption-risks")
def disruption_risks():

    query = """
    SELECT
      sk.sku_name,
      sk.category,
      ip.closing_stock_units,
      ip.days_of_cover,
      sk.reorder_point_units,
      CASE
        WHEN ip.days_of_cover < 7
        THEN 'Critical'
        WHEN ip.days_of_cover < 14
        THEN 'Warning'
        ELSE 'Monitor'
      END as urgency
    FROM skus sk
    JOIN inventory_positions ip
      ON sk.sku_id = ip.sku_id
    WHERE ip.date = (
      SELECT MAX(date)
      FROM inventory_positions
    )
    AND ip.days_of_cover < 14
    ORDER BY ip.days_of_cover ASC
    LIMIT 20
    """

    result = pd.read_sql(query, engine)

    return result.to_dict(orient='records')


@app.get("/api/analytics/supplier-risks")
def supplier_risks():

    query = """
    SELECT
      s.supplier_id,
      s.city_tier,
      sp.otif_percentage as current_otif,
      sp.avg_lead_time_days,
      sp.fill_rate_pct
    FROM suppliers s
    JOIN supplier_performance sp
      ON s.supplier_id = sp.supplier_id
    WHERE sp.month = (
      SELECT MAX(month)
      FROM supplier_performance
    )
    AND sp.otif_percentage < 75
    ORDER BY sp.otif_percentage ASC
    LIMIT 10
    """

    result = pd.read_sql(query, engine)

    return result.to_dict(orient='records')


@app.get("/api/analytics/forecast-accuracy")
def forecast_accuracy():

    try:

        # Load last 30 days WITH date, sorted
        df = pd.read_sql("""
    SELECT
        sku_id,
        date::date,
        quantity_demanded
    FROM demand_history
    WHERE date::date >= (
        SELECT MAX(date::date) FROM demand_history
    ) - INTERVAL '30 days'
    ORDER BY sku_id, date::date
""", engine)

        # Rolling 7-day average as forecast (stable, avoids 100%+ MAPE)
        df['forecast'] = (
            df.groupby('sku_id')['quantity_demanded']
            .transform(lambda x: x.rolling(window=30, min_periods=7).mean().shift(1))
        )

        # Remove nulls and zero actuals
        df = df.dropna()
        df = df[df['quantity_demanded'] != 0]

        # Calculate APE
        df['ape'] = (
            abs(df['quantity_demanded'] - df['forecast'])
            / df['quantity_demanded'] * 100
        )

        # MAPE per SKU
        result = df.groupby('sku_id')['ape'].mean().reset_index()
        result.rename(columns={'ape': 'mape_30day'}, inplace=True)
        

        # Remove inf and NaN from MAPE
        result = result.replace([np.inf, -np.inf], np.nan)
        result = result.dropna(subset=['mape_30day'])

        # Add SKU details
        sku_info = pd.read_sql("""
            SELECT sku_id, sku_name, category
            FROM skus
        """, engine)

        result = result.merge(sku_info, on='sku_id', how='left')

        # Accuracy tiers
        result['accuracy_tier'] = result['mape_30day'].apply(
            lambda x:
                "Excellent"         if x < 15 else
                "Good"              if x < 25 else
                "Needs Improvement"
        )

        # Convert to records and clean any remaining inf/nan
        skus_list = result.to_dict(orient='records')
        for sku in skus_list:
            for key, val in sku.items():
                if isinstance(val, float) and (math.isnan(val) or math.isinf(val)):
                    sku[key] = None

        # Clean avg_mape
        avg_mape = result['mape_30day'].mean()
        if math.isnan(avg_mape) or math.isinf(avg_mape):
            avg_mape = 0.0

        return {
            "report_date":  str(date.today()),
            "total_skus":   int(len(result)),
            "avg_mape":     float(round(avg_mape, 2)),
            "skus":         skus_list
        }

    except Exception as e:
        return {"error": str(e)}


@app.get("/api/analytics/inventory-summary")
def inventory_summary():

    try:

        summary = pd.read_sql("""
            SELECT
                COUNT(DISTINCT sku_id)
                    as total_skus_tracked,
                SUM(
                    CASE
                        WHEN days_of_cover < 14
                        THEN 1
                        ELSE 0
                    END
                ) as critical_skus,
                SUM(
                    CASE
                        WHEN days_of_cover >= 14
                        AND days_of_cover < 30
                        THEN 1
                        ELSE 0
                    END
                ) as warning_skus,
                SUM(
                    CASE
                        WHEN days_of_cover >= 30
                        THEN 1
                        ELSE 0
                    END
                ) as healthy_skus,
                ROUND(
                    AVG(days_of_cover)::numeric,
                    1
                ) as avg_days_of_cover
            FROM inventory_positions
            WHERE date = (
                SELECT MAX(date)
                FROM inventory_positions
            )
        """, engine)

        top_critical = pd.read_sql("""
            SELECT
                sk.sku_name,
                ip.days_of_cover
            FROM inventory_positions ip
            JOIN skus sk
                ON ip.sku_id = sk.sku_id
            WHERE ip.date = (
                SELECT MAX(date)
                FROM inventory_positions
            )
            ORDER BY ip.days_of_cover ASC
            LIMIT 3
        """, engine)

        return {
            "report_date": str(date.today()),
            "total_skus_tracked":
                int(summary.iloc[0]['total_skus_tracked']),
            "critical_skus":
                int(summary.iloc[0]['critical_skus']),
            "warning_skus":
                int(summary.iloc[0]['warning_skus']),
            "healthy_skus":
                int(summary.iloc[0]['healthy_skus']),
            "total_inventory_value": 0,
            "stockout_risk_value": 0,
            "avg_days_of_cover":
                float(summary.iloc[0]['avg_days_of_cover']),
            "top_3_critical":
                top_critical.to_dict(orient='records')
        }

    except Exception as e:
        return {"error": str(e)}


uvicorn.run(app, host="0.0.0.0", port=8001)
