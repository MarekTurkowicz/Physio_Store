"""
Tests for PhysioShop API.
Uses httpx AsyncClient with FastAPI TestClient.
"""

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest_asyncio.fixture
async def client():
    """Async HTTP client for testing."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """Health endpoint should return 200 with app info."""
    response = await client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["app_name"] == "PhysioShop"


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    """Should register a new user and return user data."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpass123",
            "full_name": "Test User",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["role"] == "customer"
    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    """Should reject duplicate email registration."""
    user_data = {
        "email": "duplicate@example.com",
        "password": "testpass123",
        "full_name": "Duplicate User",
    }
    await client.post("/api/v1/auth/register", json=user_data)
    response = await client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    """Should login and return JWT token."""
    # Register first
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "login_test@example.com",
            "password": "mypassword",
            "full_name": "Login Test",
        },
    )
    # Login
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "login_test@example.com", "password": "mypassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    """Should reject wrong password."""
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "wrong_pw@example.com",
            "password": "correct_pass",
            "full_name": "Wrong PW",
        },
    )
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "wrong_pw@example.com", "password": "wrong_pass"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_profile_unauthorized(client: AsyncClient):
    """Should reject request without token."""
    response = await client.get("/api/v1/users/me")
    assert response.status_code == 422  # Missing required header


@pytest.mark.asyncio
async def test_get_profile_with_token(client: AsyncClient):
    """Should return user profile with valid token."""
    # Register + Login
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "profile@example.com",
            "password": "profilepass",
            "full_name": "Profile User",
        },
    )
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "profile@example.com", "password": "profilepass"},
    )
    token = login_resp.json()["access_token"]

    # Get profile
    response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "profile@example.com"


@pytest.mark.asyncio
async def test_list_products_empty(client: AsyncClient):
    """Should return empty product list."""
    response = await client.get("/api/v1/products/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 0
    assert isinstance(data["items"], list)


@pytest.mark.asyncio
async def test_list_categories_empty(client: AsyncClient):
    """Should return categories list."""
    response = await client.get("/api/v1/categories/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["items"], list)
