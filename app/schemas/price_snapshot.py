from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


class PriceSnapshotResponse(BaseModel):
    id: int
    symbol: str
    price: Decimal
    recorded_at: datetime

    model_config = {"from_attributes": True}
