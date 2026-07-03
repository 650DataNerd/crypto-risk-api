from pydantic import BaseModel
from datetime import datetime


class PortfolioCreate(BaseModel):
    name: str


class PortfolioResponse(BaseModel):
    id: int
    user_id: int
    name: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
