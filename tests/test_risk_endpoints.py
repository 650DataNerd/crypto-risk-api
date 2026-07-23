from decimal import Decimal
from app.models.price_snapshot import PriceSnapshot


async def test_latest_price_returns_404_for_unknown_symbol(auth_client):
    response = await auth_client.get("/risk/prices/UNKNOWN")
    assert response.status_code == 404


async def test_latest_price_requires_auth(client):
    response = await client.get("/risk/prices/BTC")
    assert response.status_code == 401


async def test_risk_metrics_requires_auth(client):
    response = await client.get("/risk/BTC")
    assert response.status_code == 401


async def test_risk_metrics_insufficient_data(auth_client):
    response = await auth_client.get("/risk/DOGE")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["data_points"] == 0


async def test_risk_metrics_with_data(auth_client, db_session):
    for price in [60000, 62000, 61000, 65000, 63000]:
        db_session.add(PriceSnapshot(symbol="TESTBTC", price=Decimal(str(price))))
    await db_session.flush()

    response = await auth_client.get("/risk/TESTBTC")
    assert response.status_code == 200
    data = response.json()
    assert data["data_points"] == 5
    assert data["volatility"] is not None
    assert data["max_drawdown_pct"] is not None
