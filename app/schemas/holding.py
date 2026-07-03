from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


class HoldingCreate(BaseModel):
    symbol: str
    amount: Decimal


class HoldingResponse(BaseModel):
    id: int
    portfolio_id: int
    symbol: str
    amount: Decimal
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
