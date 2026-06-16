import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from datetime import datetime
from groq import Groq
from sqlalchemy import create_engine
import re
import time

# ===================================================
# GROQ CLIENT
# ===================================================



load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
# ===================================================
# FASTAPI APP
# ===================================================

app = FastAPI(
    title="SupplyMind AI Response Engine",
    description="AI-powered supply chain disruption response API",
    version="1.0"
)

# ===================================================
# CORS CONFIGURATION
# ===================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===================================================
# INPUT MODEL
# ===================================================

class DisruptionRequest(BaseModel):
    disruption_type: str
    sku_name: str
    category: str
    closing_stock_units: int
    daily_consumption_units: int
    days_of_cover: float
    otif_percentage: float
    lead_time_days: int
    alternate_supplier: str


# ===================================================
# REORDER QUANTITY CALCULATION
# ===================================================

def calculate_reorder_qty(
    daily_demand,
    lead_time_days=7,
    safety_buffer=1.2
):
    reorder = daily_demand * 30 * safety_buffer
    lead_time_cover = daily_demand * lead_time_days
    total = reorder + lead_time_cover

    return round(total)


# ===================================================
# RESPONSE PLAN GENERATOR
# ===================================================

def generate_response_plan(d: dict) -> dict:

    reorder_qty = calculate_reorder_qty(
        d['daily_consumption_units'],
        d['lead_time_days']
    )

    # ===================================================
    # SCENARIO-SPECIFIC INSTRUCTIONS
    # ===================================================

    extra_instruction = ""

    # Scenario 1
    if d['disruption_type'] == "Supplier Delivery Failure":

        extra_instruction = """
Focus on:
- Alternate supplier activation
- Emergency replenishment
- Minimizing operational disruption
"""

    # Scenario 2
    elif d['disruption_type'] == "Critical Stockout Risk":

        extra_instruction = """
Focus on:
- Immediate inventory replenishment
- Preventing stock depletion
- Continuous inventory monitoring
"""

    # Scenario 3
    elif d['disruption_type'] == "Demand Spike Above Forecast":

        extra_instruction = """
Focus on:
- Increasing reorder quantity
- Faster replenishment
- Alternate suppliers with faster delivery
- Preventing future stock shortages
"""

    # Scenario 4
    elif d['disruption_type'] == "Lead Time Suddenly Increased":

        extra_instruction = """
Focus on:
- Advancing reorder dates
- Increasing safety stock
- Managing delayed supplier deliveries
- Maintaining inventory coverage
"""

    # Scenario 5
    elif d['disruption_type'] == "Inventory Instability":

        extra_instruction = """
Focus on:
- Supply chain stabilization
- Inventory continuity
- Reducing inventory fluctuations
"""

    else:

        extra_instruction = """
Focus on:
- Supply chain stabilization
- Inventory continuity
"""

    # ===================================================
    # AI PROMPT
    # ===================================================

    prompt = f"""
You are a supply chain manager.

Disruption Type:
{d['disruption_type']}

Scenario Instructions:
{extra_instruction}

SKU: {d['sku_name']}
Category: {d['category']}

Current Stock: {d['closing_stock_units']} units
Daily Demand: {d['daily_consumption_units']} units/day
Days of Cover: {d['days_of_cover']} days
Supplier OTIF: {d['otif_percentage']}%
Lead Time: {d['lead_time_days']} days

Alternate Supplier:
{d['alternate_supplier']}

STRICT RULES:
- Only use supplier IDs from Alternate Supplier field
- Reorder Quantity is exactly {reorder_qty} units
- Do not invent supplier IDs
- Use only numbers provided above

Write:
1. Situation Summary (2 sentences)
2. Immediate Actions (3 points)
3. Alternate Supplier Recommendation
4. Reorder Quantity
5. Monitoring Checklist (3 points)
"""

    # ===================================================
    # GENERATION TIMER
    # ===================================================

    start = time.time()

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=600,
        temperature=0.3,
    )

    end = time.time()

    generation_time = round(end - start, 2)

    plan = response.choices[0].message.content

    # ===================================================
    # HALLUCINATION VALIDATION
    # ===================================================

    sup_ids = re.findall(r'SUP-\d+', plan)

    allowed = re.findall(
        r'SUP-\d+',
        d['alternate_supplier']
    )

    invented = [
        s for s in sup_ids
        if s not in allowed
    ]

    # ===================================================
    # FINAL RESPONSE
    # ===================================================

    return {
        "plan": plan,
        "reorder_qty": reorder_qty,
        "is_clean": len(invented) == 0,
        "hallucinated": invented,
        "generation_time_seconds": generation_time
    }

# ===================================================
# EXECUTIVE BRIEFING GENERATOR
# ===================================================

def generate_executive_briefing(date: str):

    suppliers = pd.read_csv("data/raw/suppliers.csv")
    supplier_perf = pd.read_csv("data/raw/supplier_performance.csv")
    inventory = pd.read_csv("data/raw/inventory_positions.csv")
    supplier_perf = supplier_perf.drop_duplicates(subset=["supplier_id"])

    at_risk = supplier_perf.nsmallest(
        5,
        "otif_percentage"
    )

    seen = set()
    at_risk_suppliers = []

    for _, row in at_risk.iterrows():

            if row["supplier_id"] in seen:
                continue
            seen.add(row["supplier_id"])

            at_risk_suppliers.append({
                "supplier_id": row["supplier_id"],
                "current_risk": "High",
                "reason": f"OTIF dropped to {round(row['otif_percentage'],2)}%"
    })
    improving_suppliers = []

    improving = supplier_perf.nlargest(
        3,
        "otif_percentage"
    )

    for _, row in improving.iterrows():

        improving_suppliers.append({
            "supplier_id": row["supplier_id"],
            "improvement": "Strong OTIF performance"
        })

    inventory_alerts = []

    low_stock = inventory[
        inventory["closing_stock_units"] < 100
    ]

    for _, row in low_stock.head(5).iterrows():

        inventory_alerts.append({
            "sku": row["sku_id"],
            "alert": "Low Stock Risk"
        })

    avg_otif = round(
        supplier_perf["otif_percentage"].mean(),
        2
    )

    return {

        "date": date,

        "summary":
        f"{len(at_risk_suppliers)} suppliers at risk, "
        f"{len(improving_suppliers)} improving suppliers, "
        f"{len(inventory_alerts)} inventory alerts",

        "at_risk_suppliers":
        at_risk_suppliers,

        "improving_suppliers":
        improving_suppliers,

        "inventory_alerts":
        inventory_alerts,

        "forecast_accuracy": {
            "avg_mape": 8.2,
            "trend": "improving"
        },

        "key_insight":
        f"Average OTIF currently {avg_otif}%"
    }

# ===================================================
# FASTAPI ENDPOINT
# ===================================================

@app.post("/api/response-plan")

def response_plan(request: DisruptionRequest):

    result = generate_response_plan(
        request.dict()
    )

    return result

# ===================================================
# EXECUTIVE BRIEFING ENDPOINT
# ===================================================

@app.get("/api/analytics/executive-briefing")

def executive_briefing(date: str):

    return generate_executive_briefing(date)

# ===================================================
# DATABASE TEST ENDPOINT
# ===================================================

@app.get("/api/test-db")
def test_db():

    query = "SELECT NOW()"

    result = pd.read_sql(query, engine)

    return {
        "status": "connected",
        "time": str(result.iloc[0][0])
    }


@app.get("/api/tables")
def list_tables():

    query = """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema='public'
    """

    tables = pd.read_sql(query, engine)

    return tables.to_dict(orient="records")


# ===================================================
# ROOT ENDPOINT
# ===================================================

@app.get("/")

def home():

    return {
        "message": "SupplyMind Response Plan API Running"
    }


# ===================================================
# TEST SCENARIOS
# ===================================================

scenarios = [

    # Scenario 1
    {
        "disruption_type": "Supplier Delivery Failure",
        "sku_name": "Electronics Component 47",
        "category": "Electronics",
        "closing_stock_units": 45,
        "daily_consumption_units": 32,
        "days_of_cover": 1.4,
        "otif_percentage": 61.0,
        "lead_time_days": 14,
        "alternate_supplier": "SUP-0045 (OTIF 88%)"
    },

    # Scenario 2
    {
        "disruption_type": "Critical Stockout Risk",
        "sku_name": "Raw Materials Component 20",
        "category": "Raw Materials",
        "closing_stock_units": 120,
        "daily_consumption_units": 45,
        "days_of_cover": 2.7,
        "otif_percentage": 72.0,
        "lead_time_days": 21,
        "alternate_supplier": "SUP-0112 (OTIF 83%)"
    },

    # Scenario 3
    {
        "disruption_type": "Demand Spike Above Forecast",
        "sku_name": "Packaging Component 12",
        "category": "Packaging",
        "closing_stock_units": 980,
        "daily_consumption_units": 158,
        "days_of_cover": 6.2,
        "otif_percentage": 85.0,
        "lead_time_days": 10,
        "alternate_supplier": "SUP-0078 (OTIF 91%)"
    },

    # Scenario 4
    {
        "disruption_type": "Lead Time Suddenly Increased",
        "sku_name": "Medical Component 8",
        "category": "Healthcare",
        "closing_stock_units": 300,
        "daily_consumption_units": 40,
        "days_of_cover": 7.5,
        "otif_percentage": 79.0,
        "lead_time_days": 28,
        "alternate_supplier": "SUP-0200 (OTIF 89%)"
    },

    # Scenario 5
    {
        "disruption_type": "Inventory Instability",
        "sku_name": "Industrial Component 99",
        "category": "Industrial",
        "closing_stock_units": 500,
        "daily_consumption_units": 60,
        "days_of_cover": 8.1,
        "otif_percentage": 82.0,
        "lead_time_days": 12,
        "alternate_supplier": "SUP-0301 (OTIF 90%)"
    }

]


# ===================================================
# RUN TEST SCENARIOS
# ===================================================

if __name__ == "__main__":

    for s in scenarios:

        result = generate_response_plan(s)

        print(f"\n{'='*60}")
        print(f"SCENARIO: {s['disruption_type']}")
        print(f"{'='*60}")

        print(result['plan'])

        print(f"\nReorder Qty: {result['reorder_qty']}")
        print(f"Clean: {result['is_clean']}")
        print(f"Hallucinated: {result['hallucinated']}")
        print(
            f"Generation Time: "
            f"{result['generation_time_seconds']} seconds"
        )
