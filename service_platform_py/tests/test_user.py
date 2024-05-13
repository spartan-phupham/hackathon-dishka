import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status

from service_platform_py.api.router.user.manager import UserManager


@pytest.mark.anyio
async def test_user_creation(
    fastapi_app: FastAPI,
    client: AsyncClient,
    user_manager: UserManager,
) -> None:
    """Tests dummy instance creation."""
    url = fastapi_app.url_path_for("UserRouter.new")
    response = await client.post(
        url,
        json={
            "email": "admin@gmail.com",
            "phone": "123456",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    instances = await user_manager.by_id(data["id"])
    assert instances.email == "admin@gmail.com"

    instances = await user_manager.by_email("admin@gmail.com")
    assert instances.email == "admin@gmail.com"
