import ollama
import re
import time
def calculate_reorder_qty(
        daily_demand,
        lead_time_days=7,
        safety_buffer=1.2):

    reorder = daily_demand * 30 * safety_buffer

    lead_time_cover = daily_demand * lead_time_days

    total = reorder + lead_time_cover

    return round(total)


def generate_response_plan(d: dict) -> dict:

    reorder_qty = calculate_reorder_qty(
        d['daily_consumption_units'],
        d.get('lead_time_days', 7)
    )

    prompt = f"""
You are a supply chain manager.

Disruption: {d['type']}
SKU: {d['sku_name']} (Category: {d['category']})

Current Stock: {d['closing_stock_units']} units
Daily Demand: {d['daily_consumption_units']} units/day
Days of Cover: {d['days_of_cover']} days
Supplier OTIF: {d['otif_percentage']}%
Lead Time: {d.get('lead_time_days', 7)} days

Alternate: {d['alternate_supplier']}

STRICT RULES:
- Only use supplier IDs from Alternate field
- Reorder Quantity is exactly {reorder_qty} units
- Use only numbers from above

Write:
1. Situation Summary (2 sentences)
2. Immediate Actions (3 points)
3. Alternate Supplier (only {d['alternate_supplier']})
4. Reorder Quantity: {reorder_qty} units
5. Monitoring Checklist (3 items)
"""

    response = ollama.chat(
        model='llama3',
        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ]
    )

    plan = response['message']['content']

    # Validation
    sup_ids = re.findall(r'SUP-\d+', plan)

    allowed = re.findall(
        r'SUP-\d+',
        d['alternate_supplier']
    )

    invented = [
        s for s in sup_ids
        if s not in allowed
    ]

    return {
        'plan': plan,
        'reorder_qty': reorder_qty,
        'is_clean': len(invented) == 0,
        'hallucinated': invented
    }


# Test Scenarios
scenarios = [

    {
        'type': 'Supplier Delivery Failure',
        'sku_name': 'Electronics Component 47',
        'category': 'Electronics',
        'closing_stock_units': 45,
        'daily_consumption_units': 32,
        'days_of_cover': 1.4,
        'otif_percentage': 61.0,
        'lead_time_days': 14,
        'alternate_supplier': 'SUP-0045 (OTIF 88%)'
    },

    {
        'type': 'Critical Stockout Risk',
        'sku_name': 'Raw Materials Component 20',
        'category': 'Raw Materials',
        'closing_stock_units': 120,
        'daily_consumption_units': 45,
        'days_of_cover': 2.7,
        'otif_percentage': 72.0,
        'lead_time_days': 21,
        'alternate_supplier': 'SUP-0112 (OTIF 83%)'
    }

]


# Run Scenarios
for s in scenarios:

    print(f"\n{'=' * 50}")
    print(f"SCENARIO: {s['type']}")
    print(f"{'=' * 50}")

    start = time.time()

    result = generate_response_plan(s)

    end = time.time()

    total_time = round(end - start, 2)

    print(result['plan'])

    print(f"\nReorder Qty: {result['reorder_qty']}")

    print(f"Clean: {result['is_clean']}")

    print(f"Hallucinated: {result['hallucinated']}")

    print(f"\nGeneration Time: {total_time} seconds")