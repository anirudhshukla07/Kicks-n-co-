import secrets
from datetime import datetime, timedelta
from passlib.context import CryptContext
from app.core.config import get_settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
settings = get_settings()


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def generate_session_token() -> str:
    return secrets.token_urlsafe(48)


def get_session_expiry() -> datetime:
    return datetime.utcnow() + timedelta(hours=settings.session_expire_hours)
