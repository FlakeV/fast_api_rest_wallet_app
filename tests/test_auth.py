from httpx import AsyncClient

DEFAULT_USER = {
    "username": "test",
    "email": "test@test.com",
    "password": "longpassword",
    "phone": "+79999999999",
}


async def test_sign_up(ac: AsyncClient):
    response = await ac.post(
        "/auth/sign-up",
        json=DEFAULT_USER,
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


async def test_sign_up_error_same_email(ac: AsyncClient):
    response = await ac.post(
        "/auth/sign-up",
        json=DEFAULT_USER,
    )
    assert response.status_code == 400
    assert f"User with {DEFAULT_USER['email']} email already exists" in response.text
