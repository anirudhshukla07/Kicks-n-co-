from datetime import datetime
from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    brand: Mapped[str] = mapped_column(String(80), nullable=False)
    name: Mapped[str] = mapped_column(String(180), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    resell_price: Mapped[float] = mapped_column(Float, nullable=False)
    badge: Mapped[str] = mapped_column(String(40), nullable=False)
    image_url: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
