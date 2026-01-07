import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
ORGANIZER_EMAIL = os.getenv("ORGANIZER_EMAIL")

def send_feedback_email(subject: str, body: str):
    msg = MIMEMultipart()
    msg["From"] = SMTP_EMAIL
    msg["To"] = ORGANIZER_EMAIL
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)
