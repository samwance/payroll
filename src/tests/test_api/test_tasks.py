from typing import Callable
from httpx import AsyncClient
from models.user import User
from models.task import Task
from schemas.task import TaskCreate, TaskUpdate
from utils.password import hash_password

ROOT_ENDPOINT = "/tasks/"

class TestTaskApi:
    async def test_create_task(self, http_client: AsyncClient, user_fixture: User, get_auth_headers: Callable):
        auth_headers = await get_auth_headers(user_fixture)

        new_task_data = TaskCreate(
            title="New Task",
            description="Task description",
            due_date="2024-12-31T23:59:59",
        )

        response = await http_client.post(ROOT_ENDPOINT, json=new_task_data.model_dump(), headers=auth_headers)
        assert response.status_code == 201
        response_data = response.json()
        assert response_data["title"] == new_task_data.title

    async def test_list_tasks(self, http_client: AsyncClient, user_fixture: User, task_fixture: Task, get_auth_headers: Callable):
        auth_headers = await get_auth_headers(user_fixture)
        response = await http_client.get(ROOT_ENDPOINT, headers=auth_headers)
        assert response.status_code == 200
        response_data = response.json()
        assert isinstance(response_data["tasks"], list)

    async def test_get_task(self, http_client: AsyncClient, user_fixture: User, get_auth_headers: Callable, task_fixture: Task):
        auth_headers = await get_auth_headers(user_fixture)
        response = await http_client.get(f"{ROOT_ENDPOINT}{task_fixture.id}/", headers=auth_headers)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["id"] == task_fixture.id

    async def test_get_task_not_found(self, http_client: AsyncClient, user_fixture: User, get_auth_headers: Callable):
        auth_headers = await get_auth_headers(user_fixture)
        response = await http_client.get(f"{ROOT_ENDPOINT}99999/", headers=auth_headers)
        assert response.status_code == 404

    async def test_update_task(self, http_client: AsyncClient, user_fixture: User, get_auth_headers: Callable, task_fixture: Task):
        auth_headers = await get_auth_headers(user_fixture)
        update_data = TaskUpdate(
            title="Updated Task Title",
            description="Updated task description",
        )
        response = await http_client.patch(f"{ROOT_ENDPOINT}{task_fixture.id}/", json=update_data.model_dump(exclude_unset=True), headers=auth_headers)
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["title"] == update_data.title

    async def test_delete_task(self, http_client: AsyncClient, user_fixture: User, get_auth_headers: Callable, task_fixture: Task):
        auth_headers = await get_auth_headers(user_fixture)
        response = await http_client.delete(f"{ROOT_ENDPOINT}{task_fixture.id}/", headers=auth_headers)
        assert response.status_code == 204

    async def test_delete_task_not_found(self, http_client: AsyncClient, user_fixture: User, get_auth_headers: Callable):
        auth_headers = await get_auth_headers(user_fixture)
        response = await http_client.delete(f"{ROOT_ENDPOINT}99999/", headers=auth_headers)
        assert response.status_code == 404

    async def test_delete_task_forbidden(self, http_client: AsyncClient, user_fixture: User, get_auth_headers: Callable, task_fixture: Task):
        non_creator_user = User(username="non_creator", is_admin=False)
        auth_headers = await get_auth_headers(non_creator_user)
        response = await http_client.delete(f"{ROOT_ENDPOINT}{task_fixture.id}/", headers=auth_headers)
        assert response.status_code == 403
