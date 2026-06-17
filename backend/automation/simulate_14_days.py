import requests
from datetime import datetime, timedelta

API_URL = (
    "https://supplymind-response-engine.onrender.com"
    "/api/analytics/executive-briefing"
)

for i in range(14):

    day = (
        datetime.now()
        - timedelta(days=i + 1)
    ).strftime("%Y-%m-%d")

    print(f"Testing {day}...")

    response = requests.get(
        API_URL,
        params={"date": day}
    )

    if response.status_code == 200:

        print(f"{day} - PASS")

    else:

        print(f"{day} - FAIL")
