import os
import requests

EMAIL_API_URL = os.getenv("EMAIL_API_URL", "http://localhost:3020/api/email")

# credentials to use as sender
EMAIL_USER = os.getenv("EMAIL_USER")  # your Gmail address
EMAIL_PASS = os.getenv("EMAIL_PASS")  # app password


def queue_email(to: str, subject: str, text: str):
    if not EMAIL_USER or not EMAIL_PASS:
        raise RuntimeError("EMAIL_USER/EMAIL_PASS not configured")
    
    payload = {
        "to": to,
        "subject": subject,
        "text": text,
        "emailUser": EMAIL_USER,
        "emailPass": EMAIL_PASS,
    }

    resp = requests.post(EMAIL_API_URL, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()
