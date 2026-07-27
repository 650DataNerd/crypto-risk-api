from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class PriceSnapshotResponse(BaseModel):
    id: int
    symbol: str
    price: Decimal
    recorded_at: datetime

    model_config = {"from_attributes": True}
