# src/utils/mailer.py
import os
import smtplib
from email.mime.text import MIMEText

SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
TO_EMAIL = os.getenv("FEEDBACK_RECEIVER_EMAIL")

def send_feedback_email(subject: str, body: str):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_EMAIL
    msg["To"] = TO_EMAIL

    with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as server:
        server.starttls()          # 🔑 THIS is critical
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)
