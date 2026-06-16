# SupplyMind API Documentation

## Endpoint: Response Plan API

### API Name

AI-Powered Disruption Response Plan Generator

---

# Base URL

```http
http://127.0.0.1:8000
```

---

# Endpoint

```http
POST /api/response-plan
```

---

# Purpose

This API generates AI-powered supply chain disruption response plans using live disruption data.

The system analyzes:

* Inventory levels
* Supplier performance
* Demand spikes
* Lead times
* Alternate suppliers

and produces:

* Situation summary
* Immediate actions
* Alternate supplier recommendation
* Reorder quantity
* Monitoring checklist

---

# Request Format

## Headers

```json
Content-Type: application/json
```

---

# Request Body Example

```json
{
  "disruption_type": "Critical Stockout Risk",
  "sku_name": "Electronics Component",
  "category": "Electronics",
  "closing_stock_units": 120,
  "daily_consumption_units": 60,
  "days_of_cover": 2,
  "otif_percentage": 83,
  "lead_time_days": 7,
  "alternate_supplier": "SUP-0112"
}
```

---

# Parameters

| Parameter               | Type    | Description                       |
| ----------------------- | ------- | --------------------------------- |
| disruption_type         | string  | Type of supply chain disruption   |
| sku_name                | string  | SKU/Product name                  |
| category                | string  | Product category                  |
| closing_stock_units     | integer | Current available stock           |
| daily_consumption_units | integer | Daily demand                      |
| days_of_cover           | float   | Number of inventory coverage days |
| otif_percentage         | float   | Supplier OTIF performance         |
| lead_time_days          | integer | Supplier lead time                |
| alternate_supplier      | string  | Backup supplier ID                |

---

# Successful Response Example

```json
{
  "plan": "Generated AI response plan...",
  "reorder_qty": 2580,
  "is_clean": true,
  "hallucinated": [],
  "generation_time_seconds": 0.97
}
```

---

# Response Fields

| Field                   | Description                      |
| ----------------------- | -------------------------------- |
| plan                    | AI-generated disruption response |
| reorder_qty             | Calculated reorder quantity      |
| is_clean                | Hallucination validation result  |
| hallucinated            | Invalid supplier IDs detected    |
| generation_time_seconds | API response time                |

---

# Error Codes

| Status Code | Meaning               |
| ----------- | --------------------- |
| 200         | Success               |
| 400         | Invalid input         |
| 404         | Resource not found    |
| 500         | Internal server error |

---

# Performance Metrics

| Metric                | Result       |
| --------------------- | ------------ |
| Average Response Time | 1.2 seconds  |
| Max Response Time     | 1.99 seconds |
| Error Rate            | 0%           |
| Concurrent Testing    | Passed       |

---

# Dependencies

## Python Libraries

* FastAPI
* Uvicorn
* Groq
* Pydantic

---

# Environment Variables

```env
GROQ_API_KEY=your_api_key
```

---

# Run Instructions

## Activate Virtual Environment

```bash
.venv\Scripts\activate
```

## Start Server

```bash
uvicorn main:app --reload
```

---

# Swagger Documentation

```http
http://127.0.0.1:8000/docs
```

---

# Known Limitations

* Requires internet connection for Groq API
* AI responses may vary slightly
* Depends on external LLM availability

---

# Developed By

Subramanyam Karthi — SupplyMind Backend Team
