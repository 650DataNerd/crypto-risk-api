from app.schemas.portfolio import PortfolioCreate, PortfolioResponse
from datetime import datetime


def create_portfolio(data: PortfolioCreate) -> PortfolioResponse:
    return PortfolioResponse(
        id=1,
        user_id=1,
        name=data.name,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


def get_portfolios() -> list[PortfolioResponse]:
    return [
        PortfolioResponse(
            id=1,
            user_id=1,
            name="My First Portfolio",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
    ]
