from typing import Callable
from httpx import AsyncClient
from models.user import User
from schemas.user import UserCreate, UserUpdate
from src.utils.password import hash_password

ROOT_ENDPOINT = "/payroll/"

class TestUserApi:
    async def test_create_user(self, http_client: AsyncClient, user_fixture: User, get_auth_headers: Callable):
        admin_auth_headers = await get_auth_headers(user_fixture)
        
        new_user_data = UserCreate(
            name="Another_user",
            second_name="User",
            surname='Another',
            phone="11111111",
            position='jun',
            password=hash_password("password123"),
            random_password='password123',
            salary=10000,
        )
        
        response = await http_client.post(ROOT_ENDPOINT, json=new_user_data.model_dump(), headers=admin_auth_headers)
        assert response.status_code == 201
        response_data = response.json()
        assert response_data["phone"] == new_user_data.phone

    async def test_create_user_forbidden(self, http_client: AsyncClient, user_fixture_2: User, get_auth_headers: Callable):
        non_admin_auth_headers = await get_auth_headers(user_fixture_2)
        
        new_user_data = UserCreate(
            name="Another_user",
            second_name="User",
            surname='Another',
            phone="11111111",
            position='jun',
            password=hash_password("password123"),
            random_password='password123',
            salary=10000,
        )
        
        response = await http_client.post(ROOT_ENDPOINT, json=new_user_data.model_dump(), headers=non_admin_auth_headers)
        assert response.status_code == 403

    async def test_list_users(self, http_client: AsyncClient, user_fixture: User, get_auth_headers: Callable):
        auth_headers = await get_auth_headers(user_fixture)
        response = await http_client.get(f"{ROOT_ENDPOINT}users/", headers=auth_headers)
        assert response.status_code == 200
        response_data = response.json()
        assert isinstance(response_data["users"], list)

    async def test_get_user_profile(self, http_client: AsyncClient, user_fixture: User, get_auth_headers: Callable):
        auth_headers = await get_auth_headers(user_fixture)
        response = await http_client.get(f"{ROOT_ENDPOINT}profile/", headers=auth_headers)
        assert response.status_code == 200
        response_data = response.json()
        assert user_fixture.id == response_data["id"]

    async def test_get_user_by_id(self, http_client: AsyncClient, user_fixture: User, get_auth_headers: Callable):
        auth_headers = await get_auth_headers(user_fixture)
        response = await http_client.get(f"{ROOT_ENDPOINT}users/{user_fixture.id}/", headers=auth_headers)
        assert response.status_code == 200
        response_data = response.json()
        assert user_fixture.id == response_data["id"]

    async def test_get_user_by_id_not_found(self, http_client: AsyncClient, user_fixture: User, get_auth_headers: Callable):
        auth_headers = await get_auth_headers(user_fixture)
        response = await http_client.get(f"{ROOT_ENDPOINT}users/99999/", headers=auth_headers)
        assert response.status_code == 404

    async def test_update_user(self, http_client: AsyncClient, user_fixture: User, get_auth_headers: Callable):
        auth_headers = await get_auth_headers(user_fixture)
        update_data = UserUpdate(
            name="UpdatedFirstName"
        )
        response = await http_client.put(f"{ROOT_ENDPOINT}users/", json=update_data.model_dump(exclude_unset=True), headers=auth_headers)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["name"] == update_data.name
        assert response_data["second_name"] == user_fixture.second_name
