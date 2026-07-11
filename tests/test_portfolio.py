import pytest


async def test_list_portfolios_returns_200(client, test_user):
    response = await client.get("/portfolios/")
    assert response.status_code == 200


async def test_list_portfolios_returns_list(client, test_user):
    response = await client.get("/portfolios/")
    data = response.json()
    assert isinstance(data, list)


async def test_create_portfolio_returns_201(client, test_user):
    response = await client.post("/portfolios/", json={"name": "Test Portfolio"})
    assert response.status_code == 201


async def test_create_portfolio_returns_correct_name(client, test_user):
    response = await client.post("/portfolios/", json={"name": "My BTC Portfolio"})
    data = response.json()
    assert data["name"] == "My BTC Portfolio"
