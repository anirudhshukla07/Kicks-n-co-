from datetime import datetime
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base


class NewsletterSubscriber(Base):
    __tablename__ = 'newsletter_subscribers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
