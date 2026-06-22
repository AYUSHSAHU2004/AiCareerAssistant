import requests
from app.config import settings


def queue_email(to: str, subject: str, text: str):
    url = settings.EMAIL_API_URL
    print(settings.EMAIL_USER)
    print(settings.EMAIL_PASS)

    payload = {
        "to": to,
        "subject": subject,
        "text": text,
        "emailUser": settings.EMAIL_USER,
        "emailPass": settings.EMAIL_PASS,
    }

    response = requests.post(url, json=payload)

    return response.json()
