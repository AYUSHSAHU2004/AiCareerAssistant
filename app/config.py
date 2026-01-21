from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Career Assistant API"
    DATABASE_URL: str
    EMAIL_API_URL: str | None = "http://localhost:3020/api/email"
    EMAIL_USER: str | None = None
    EMAIL_PASS: str | None = None

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
