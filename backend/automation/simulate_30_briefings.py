import requests
from datetime import datetime, timedelta

API_URL = (
    "https://supplymind-response-engine.onrender.com"
    "/api/analytics/executive-briefing"
)

success = 0
failures = 0

print("========== 30 BRIEFING TEST ==========\n")

for i in range(30):

    day = (
        datetime.now()
        - timedelta(days=i + 1)
    ).strftime("%Y-%m-%d")

    response = requests.get(
        API_URL,
        params={"date": day}
    )

    if response.status_code == 200:

        success += 1

        print(f"{day}  PASS")

    else:

        failures += 1

        print(f"{day}  FAIL")

print("\n==============================")
print(f"Successful Briefings : {success}")
print(f"Failed Briefings     : {failures}")
print("==============================")