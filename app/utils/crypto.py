from app.config import settings
from cryptography.fernet import Fernet

cipher = Fernet(settings.FERNET_KEY.encode())


def encrypt(text: str) -> str:
    """
    Encrypt plain text and return an encrypted string.
    """
    return cipher.encrypt(text.encode()).decode()


def decrypt(text: str) -> str:
    """
    Decrypt an encrypted string and return plain text.
    """
    return cipher.decrypt(text.encode()).decode()
