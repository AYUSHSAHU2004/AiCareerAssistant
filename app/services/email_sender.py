import requests
from app.config import settings


def queue_email(
    sender_email: str,
    sender_password: str,
    to: str,
    subject: str,
    text: str,
):
    url = settings.EMAIL_API_URL

    payload = {
        "to": to,
        "subject": subject,
        "text": text,
        "emailUser": sender_email,
        "emailPass": sender_password,
    }

    response = requests.post(url, json=payload)

    return response.json()
