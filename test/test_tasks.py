import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_task_success(
        async_client: AsyncClient, prepare_database
):
    response = await async_client.post("/tasks/", json={"title": "Test task"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test task"
    assert data["completed"] is False


@pytest.mark.asyncio
async def test_create_task_missing_title(
        async_client: AsyncClient, prepare_database
):
    response = await async_client.post("/tasks/", json={})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_tasks_empty(
        async_client: AsyncClient, prepare_database
):
    response = await async_client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    print(data)

    assert data == []
