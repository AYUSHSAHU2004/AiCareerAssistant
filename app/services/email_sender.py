import requests

def queue_email(to: str, subject: str, text: str):
    url = "http://localhost:3020/api/email"

    payload = {
        "to": to,
        "subject": subject,
        "text": text,
        "emailUser": "your_email@gmail.com",   # move later to env
        "emailPass": "your_app_password"
    }

    response = requests.post(url, json=payload)

    return response.json()