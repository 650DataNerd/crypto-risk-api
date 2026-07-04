def test_health_returns_200(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_health_returns_ok_status(client):
    response = client.get("/health")
    data = response.json()
    assert data["status"] == "ok"


def test_version_returns_200(client):
    response = client.get("/version")
    assert response.status_code == 200


def test_version_returns_correct_fields(client):
    response = client.get("/version")
    data = response.json()
    assert "name" in data
    assert "version" in data


def test_ping_returns_pong(client):
    response = client.get("/ping")
    data = response.json()
    assert data["pong"] == True
