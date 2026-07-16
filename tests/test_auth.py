async def test_register_returns_201(client):
    response = await client.post("/auth/register", json={
        "name": "New User",
        "email": "newuser@example.com",
        "password": "securepass123",
    })
    assert response.status_code == 201


async def test_register_returns_no_password(client):
    response = await client.post("/auth/register", json={
        "name": "New User",
        "email": "newuser@example.com",
        "password": "securepass123",
    })
    data = response.json()
    assert "hashed_password" not in data
    assert "password" not in data


async def test_register_duplicate_email_returns_400(client, test_user):
    response = await client.post("/auth/register", json={
        "name": "Duplicate",
        "email": "test@example.com",
        "password": "somepassword123",
    })
    assert response.status_code == 400


async def test_login_returns_token(client, test_user):
    response = await client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "testpassword123",
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


async def test_login_wrong_password_returns_401(client, test_user):
    response = await client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "wrongpassword",
    })
    assert response.status_code == 401


async def test_login_unknown_email_returns_401(client):
    response = await client.post("/auth/login", json={
        "email": "nobody@example.com",
        "password": "somepassword",
    })
    assert response.status_code == 401


async def test_protected_route_without_token_returns_401(client):
    response = await client.get("/portfolios/")
    assert response.status_code == 401
