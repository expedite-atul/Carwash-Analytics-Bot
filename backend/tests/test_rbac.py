import pytest
from backend.app.models import User, UserRole

@pytest.mark.asyncio
async def test_admin_access_admin_route(client, admin_token, session):
    # Admin accessing admin route
    response = await client.get(
        "/admin/stats/cache",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert "hits" in response.json()

@pytest.mark.asyncio
async def test_employee_denied_admin_route(client, employee_token, session):
    # Employee accessing admin route
    response = await client.get(
        "/admin/stats/cache",
        headers={"Authorization": f"Bearer {employee_token}"}
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "The user doesn't have enough privileges"

@pytest.mark.asyncio
async def test_public_route(client):
    response = await client.get("/")
    assert response.status_code == 200
