def test_list_portfolios_returns_200(client):
    response = client.get("/portfolios/")
    assert response.status_code == 200


def test_list_portfolios_returns_list(client):
    response = client.get("/portfolios/")
    data = response.json()
    assert isinstance(data, list)


def test_create_portfolio_returns_201(client):
    response = client.post("/portfolios/", json={"name": "Test Portfolio"})
    assert response.status_code == 201


def test_create_portfolio_returns_correct_name(client):
    response = client.post("/portfolios/", json={"name": "Test Portfolio"})
    data = response.json()
    assert data["name"] == "Test Portfolio"
