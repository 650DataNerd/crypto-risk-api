import httpx
import json
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.cache import set_cached
from app.models.price_snapshot import PriceSnapshot


COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"
SYMBOLS = ["bitcoin", "ethereum"]
SYMBOL_MAP = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
}


async def fetch_prices() -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            COINGECKO_URL,
            params={
                "ids": ",".join(SYMBOLS),
                "vs_currencies": "usd",
            },
            timeout=10.0,
        )
        response.raise_for_status()
        return response.json()


async def ingest_prices(db: AsyncSession) -> None:
    raw = await fetch_prices()

    for coingecko_id, symbol in SYMBOL_MAP.items():
        price_usd = raw[coingecko_id]["usd"]

        snapshot = PriceSnapshot(
            symbol=symbol,
            price=Decimal(str(price_usd)),
        )
        db.add(snapshot)

        await set_cached(
            f"price:{symbol}",
            json.dumps({"symbol": symbol, "price": str(price_usd)}),
            expire_seconds=120,
        )

    await db.commit()


async def get_latest_price(symbol: str) -> Decimal | None:
    from app.core.cache import get_cached
    cached = await get_cached(f"price:{symbol}")
    if cached:
        data = json.loads(cached)
        return Decimal(data["price"])
    return None


async def get_portfolio_value(holdings: list) -> dict:
    total_value = Decimal("0")
    breakdown = []

    for holding in holdings:
        price = await get_latest_price(holding.symbol)
        if price is None:
            continue
        value = price * holding.amount
        total_value += value
        breakdown.append({
            "symbol": holding.symbol,
            "amount": str(holding.amount),
            "price_usd": str(price),
            "value_usd": str(value),
        })

    return {
        "total_value_usd": str(total_value),
        "breakdown": breakdown,
    }
