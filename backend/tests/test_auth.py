import pytest
from backend.app.models import User

@pytest.mark.asyncio
async def test_register_user(client, session):
    response = await client.post(
        "/auth/register",
        json={
            "email": "newuser@test.com",
            "hashed_password": "password123",
            "full_name": "Test User",
            "role": "employee",
            "is_active": True
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "User created successfully"
    assert "id" in data

@pytest.mark.asyncio
async def test_login_success(client, session):
    # Create user first
    await client.post(
        "/auth/register",
        json={
            "email": "login@test.com",
            "hashed_password": "password123",
            "role": "employee"
        }
    )
    
    # Login
    response = await client.post(
        "/auth/login",
        data={"username": "login@test.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["role"] == "employee"

@pytest.mark.asyncio
async def test_login_fail(client, session):
    response = await client.post(
        "/auth/login",
        data={"username": "wrong@test.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
