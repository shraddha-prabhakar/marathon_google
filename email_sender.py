# email_sender.py
import os
import smtplib
from email.mime.text import MIMEText

SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

def send_email(to_email, subject, body_text):
    msg = MIMEText(body_text)
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = to_email

    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    server.starttls()
    server.login(SMTP_USER, SMTP_PASSWORD)
    server.sendmail(SMTP_USER, to_email, msg.as_string())
    server.quit()
