# ==========================================================
# SUPPLYMIND DAILY EXECUTIVE BRIEFING SCHEDULER
# ==========================================================
#
# Purpose:
# 1. Runs every day at 6:00 AM IST
# 2. Calls Executive Briefing API
# 3. Retrieves briefing JSON
# 4. Converts briefing into email format
# 5. Sends email to executive distribution list
# 6. Handles failures gracefully
#
# ==========================================================

from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timedelta
import requests

# Import local modules
from distribution_list import EXECUTIVE_EMAILS
from email_template import build_email
from email_sender import send_email

# ==========================================================
# CONFIGURATION
# ==========================================================

# Your deployed Render API endpoint
API_URL = (
    "https://supplymind-response-engine.onrender.com"
    "/api/analytics/executive-briefing"
)

# Gmail credentials
# Replace with your actual values
SENDER_EMAIL = "your_email@gmail.com"

# Gmail App Password
# NOT your normal Gmail password
SENDER_PASSWORD = "your_gmail_app_password"

# ==========================================================
# MAIN JOB FUNCTION
# ==========================================================

def run_daily_briefing():
    """
    Main scheduled task.

    Steps:
    1. Calculate yesterday's date
    2. Call executive briefing API
    3. Generate email content
    4. Send email to all executives
    """

    print("\n================================")
    print("Starting Daily Briefing Job")
    print("================================")

    # --------------------------------------
    # Get yesterday's date
    # --------------------------------------

    yesterday = (
        datetime.now()
        - timedelta(days=1)
    ).strftime("%Y-%m-%d")

    print(f"Generating briefing for {yesterday}")

    try:

        # --------------------------------------
        # Call Executive Briefing API
        # --------------------------------------

        response = requests.get(
            API_URL,
            params={
                "date": yesterday
            }
        )

        # Raise exception if API fails
        response.raise_for_status()

        briefing = response.json()

        print("Briefing generated successfully")

        # --------------------------------------
        # Build email content
        # --------------------------------------

        email_body = build_email(
            briefing
        )

        subject = (
            f"Daily Supply Chain Briefing - "
            f"{yesterday}"
        )

        # --------------------------------------
        # Send to executive distribution list
        # --------------------------------------

        for role, email in EXECUTIVE_EMAILS.items():

            try:

                print(
                    f"Sending email to "
                    f"{role}: {email}"
                )

                send_email(
                    recipient=email,
                    subject=subject,
                    body=email_body,
                    sender_email=SENDER_EMAIL,
                    sender_password=SENDER_PASSWORD
                )

                print(
                    f"SUCCESS: Email sent to "
                    f"{email}"
                )

            except Exception as email_error:

                print(
                    f"FAILED: Could not send "
                    f"email to {email}"
                )

                print(email_error)

        print("\nDaily briefing completed")

    except Exception as e:

        # --------------------------------------
        # Failure Handling
        # --------------------------------------

        print("\nERROR: Briefing generation failed")

        print(e)

        # Send alert email
        try:

            send_email(
                recipient=SENDER_EMAIL,
                subject="ALERT: Briefing Generation Failed",
                body=(
                    f"Briefing generation failed "
                    f"for {yesterday}.\n\n"
                    f"Manual check required."
                ),
                sender_email=SENDER_EMAIL,
                sender_password=SENDER_PASSWORD
            )

            print(
                "Failure alert email sent"
            )

        except Exception as alert_error:

            print(
                "Could not send alert email"
            )

            print(alert_error)

# ==========================================================
# APSCHEDULER SETUP
# ==========================================================

scheduler = BlockingScheduler(
    timezone="Asia/Kolkata"
)

# Schedule:
# Every day at 6:00 AM IST

scheduler.add_job(
    run_daily_briefing,
    trigger="cron",
    hour=6,
    minute=0
)

# ==========================================================
# START SCHEDULER
# ==========================================================

if __name__ == "__main__":

    print(
        "Daily Executive Briefing Scheduler Started"
    )

    print(
        "Scheduled for 6:00 AM IST"
    )

    print(
        "Waiting for next run..."
    )

    scheduler.start()

    run_daily_briefing()