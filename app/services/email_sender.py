import os
import requests

def queue_email(to: str, subject: str, text: str):
    url = os.getenv("NODE_API_URL")

    payload = {
        "to": to,
        "subject": subject,
        "text": text,
        "emailUser": os.getenv("EMAIL_USER"),
        "emailPass": os.getenv("EMAIL_PASS"),
    }

    response = requests.post(url, json=payload)

    return response.json()