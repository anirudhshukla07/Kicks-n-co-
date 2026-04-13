from datetime import datetime
from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.db.database import get_db
from app.models import User, UserSession

settings = get_settings()


def get_current_user(
    db: Session = Depends(get_db),
    session_token: str | None = Cookie(default=None, alias=settings.session_cookie_name),
) -> User:
    if not session_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authenticated')

    session = (
        db.query(UserSession)
        .filter(UserSession.session_token == session_token, UserSession.expires_at > datetime.utcnow())
        .first()
    )
    if not session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid or expired session')

    user = db.query(User).filter(User.id == session.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    return user
