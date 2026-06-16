def build_email(briefing):

    return f"""
Daily Supply Chain Briefing

Date: {briefing['date']}

Summary:
{briefing['summary']}

Key Insight:
{briefing['key_insight']}

Forecast Accuracy:
MAPE: {briefing['forecast_accuracy']['avg_mape']}
Trend: {briefing['forecast_accuracy']['trend']}

At Risk Suppliers:
{len(briefing['at_risk_suppliers'])}

Improving Suppliers:
{len(briefing['improving_suppliers'])}

Inventory Alerts:
{len(briefing['inventory_alerts'])}
"""