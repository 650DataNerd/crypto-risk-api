from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.price_snapshot import PriceSnapshot


async def get_price_history(db: AsyncSession, symbol: str, limit: int = 100) -> list[Decimal]:
    result = await db.execute(
        select(PriceSnapshot.price)
        .where(PriceSnapshot.symbol == symbol)
        .order_by(PriceSnapshot.recorded_at.asc())
        .limit(limit)
    )
    return [row[0] for row in result.fetchall()]


def compute_returns(prices: list[Decimal]) -> list[Decimal]:
    if len(prices) < 2:
        return []
    return [
        (prices[i] - prices[i - 1]) / prices[i - 1]
        for i in range(1, len(prices))
    ]


def compute_volatility(prices: list[Decimal]) -> Decimal | None:
    returns = compute_returns(prices)
    if len(returns) < 2:
        return None

    n = len(returns)
    mean = sum(returns) / n
    variance = sum((r - mean) ** 2 for r in returns) / (n - 1)
    return variance ** Decimal("0.5")


def compute_max_drawdown(prices: list[Decimal]) -> Decimal | None:
    if len(prices) < 2:
        return None

    peak = prices[0]
    max_drawdown = Decimal("0")

    for price in prices[1:]:
        if price > peak:
            peak = price
        drawdown = (price - peak) / peak
        if drawdown < max_drawdown:
            max_drawdown = drawdown

    return max_drawdown


async def get_risk_metrics(db: AsyncSession, symbol: str) -> dict:
    prices = await get_price_history(db, symbol)

    if len(prices) < 2:
        return {
            "symbol": symbol,
            "data_points": len(prices),
            "message": "Insufficient data for risk metrics",
        }

    volatility = compute_volatility(prices)
    max_drawdown = compute_max_drawdown(prices)

    return {
        "symbol": symbol,
        "data_points": len(prices),
        "volatility": str(volatility) if volatility else None,
        "max_drawdown_pct": str(max_drawdown * 100) if max_drawdown else None,
    }
