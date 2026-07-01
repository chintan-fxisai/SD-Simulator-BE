import os
from pathlib import Path
from dotenv import load_dotenv


# Definition of Root path for the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"


#Load environment variables
load_dotenv(dotenv_path=ENV_PATH)


def parse_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


#Extract variables from .env file
class Settings:

    #Application details
    APP_NAME=os.getenv("APP_NAME")
    APP_ENV=os.getenv("APP_ENV")
    API_PREFIX=os.getenv("API_PREFIX", "/api")
    FRONTEND_BASE_URL=os.getenv("FRONTEND_BASE_URL", "http://localhost:5173")
    BACKEND_BASE_URL=os.getenv("BACKEND_BASE_URL", "http://localhost:8000")

    #Database settings
    DB_NAME=os.getenv("DB_NAME")
    DB_HOST=os.getenv("DB_HOST")
    DB_USER=os.getenv("DB_USER")
    DB_PASSWORD=os.getenv("DB_PASSWORD")
    DB_PORT=os.getenv("DB_PORT")

    def construct_db_url(self) -> str:
        DB_URL: str = f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return DB_URL

    #Logger
    LOGGER_LEVEL=os.getenv("LOGGER_LEVEL")

    #JWT
    JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM=os.getenv("JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES=os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS=os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")
    SESSION_EXPIRE_DAYS=os.getenv("SESSION_EXPIRE_DAYS")

    #Email
    SMTP_HOST=os.getenv("SMTP_HOST")
    SMTP_PORT=int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME=os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD=os.getenv("SMTP_PASSWORD")
    SMTP_FROM_EMAIL=os.getenv("SMTP_FROM_EMAIL")
    SMTP_FROM_NAME=os.getenv("SMTP_FROM_NAME", APP_NAME or "Event Management System")
    SMTP_USE_TLS=parse_bool(os.getenv("SMTP_USE_TLS"), True)
    SMTP_USE_SSL=parse_bool(os.getenv("SMTP_USE_SSL"), False)
    EMAIL_VERIFICATION_EXPIRE_MINUTES=int(os.getenv("EMAIL_VERIFICATION_EXPIRE_MINUTES", "60"))
    EMAIL_VERIFICATION_PATH=os.getenv("EMAIL_VERIFICATION_PATH", f"{API_PREFIX}/auth/verify-email")


settings=Settings()

