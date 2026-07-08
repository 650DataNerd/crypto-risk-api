from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin


class Holding(Base, TimestampMixin):
    __tablename__ = "holdings"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id", ondelete="CASCADE"), nullable=False)
    symbol = Column(String, nullable=False)
    amount = Column(Numeric, nullable=False)

    portfolio = relationship("Portfolio", back_populates="holdings")
