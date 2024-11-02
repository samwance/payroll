from typing import Callable
from httpx import AsyncClient
from models.user import User
from schemas.user import UserLogin

ROOT_ENDPOINT = "/"

class TestAuthApi:
    async def test_login_success(self, http_client: AsyncClient, user_fixture: User):
        login_data = UserLogin(
            username=user_fixture.username,
            password='password123'
        )
        response = await http_client.post(f"{ROOT_ENDPOINT}login/", json=login_data.model_dump())
        # assert response.status_code == 200
        response_data = response.json()
        print(response_data)
        assert "access_token" in response_data

    async def test_login_fail(self, http_client: AsyncClient):
        login_data = UserLogin(
            username="wrong_username",
            password="wrong_password"
        )
        response = await http_client.post(f"{ROOT_ENDPOINT}login/", json=login_data.model_dump())
        assert response.status_code == 401

    async def test_logout(self, http_client: AsyncClient, user_fixture: User, get_auth_headers: Callable):
        auth_headers = await get_auth_headers(user_fixture)
        response = await http_client.delete(f"{ROOT_ENDPOINT}logout/", headers=auth_headers)
        assert response.status_code == 204

    async def test_user_not_found(self, http_client: AsyncClient, user_fixture: User, get_auth_headers: Callable):
        auth_headers = await get_auth_headers(user_fixture)
        response = await http_client.get(f"{ROOT_ENDPOINT}users/99999/", headers=auth_headers)
        assert response.status_code == 404