from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base


class UserSession(Base):
    __tablename__ = 'user_sessions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    session_token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)

    user = relationship('User', back_populates='sessions')
