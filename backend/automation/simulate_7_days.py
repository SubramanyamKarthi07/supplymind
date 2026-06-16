import requests

from datetime import datetime, timedelta

API_URL = (
    "https://supplymind-response-engine.onrender.com"
    "/api/analytics/executive-briefing"
)

for i in range(7):

    day = (
        datetime.now()
        - timedelta(days=i+1)
    ).strftime("%Y-%m-%d")

    response = requests.get(
        API_URL,
        params={"date": day}
    )

    print(
        day,
        response.status_code
    )