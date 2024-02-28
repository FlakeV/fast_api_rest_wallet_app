from httpx import AsyncClient


async def test_sign_up(async_client: AsyncClient):
    response = await async_client.post(
        "/auth/sign-up",
        json={
            "username": "test",
            "email": "test@test.com",
            "password": "longpassword",
            "phone": "+79999999999",
        },
        headers={"content-type": "application/json"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
