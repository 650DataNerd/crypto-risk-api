from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class PriceSnapshot(Base):
    __tablename__ = "price_snapshot"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, nullable=False)
    price = Column(Numeric, nullable=False)
    recorded_at = Column(DateTime, server_default=func.now(), nullable=False)
