import smtplib
from email.mime.text import MIMEText


def send_email(
    recipient,
    subject,
    body,
    sender_email,
    sender_password
):

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient

    with smtplib.SMTP(
        "smtp.gmail.com",
        587
    ) as server:

        server.starttls()

        server.login(
            sender_email,
            sender_password
        )

        server.send_message(msg)