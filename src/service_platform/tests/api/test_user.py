import pytest
from faker import Faker
from fastapi import FastAPI
from httpx import AsyncClient
from service_platform.tests.conftest import DEFAULT_USER_EMAIL

fake = Faker()


@pytest.mark.anyio
async def test_get_user_info(authenticated_client: AsyncClient, api: FastAPI) -> None:
    url = api.url_path_for("UserRouter.me")
    response = await authenticated_client.get(url)
    assert response.status_code == 200
    assert response.json()["email"] == DEFAULT_USER_EMAIL
