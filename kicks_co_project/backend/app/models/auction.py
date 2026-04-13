from datetime import datetime
from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base


class Auction(Base):
    __tablename__ = 'auctions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(180), nullable=False)
    image_url: Mapped[str] = mapped_column(Text, nullable=False)
    current_bid: Mapped[float] = mapped_column(Float, nullable=False)
    ends_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
