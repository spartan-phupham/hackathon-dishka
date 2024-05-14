import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status
from httpx import QueryParams

from service_platform_py.api.router.user.manager import UserManager
from service_platform_py.api.router.user.schema import CreateUserRequest


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


@pytest.mark.anyio
async def test_get_users(
    fastapi_app: FastAPI,
    client: AsyncClient,
    user_manager: UserManager,
) -> None:
    """Tests dummy instance creation."""
    for i in range(5):
        await user_manager.add_user(
            user=CreateUserRequest(
                email=f"admin{i}@gmail.com",
                phone=f"123456{i}",
            ),
        )
    url = fastapi_app.url_path_for("UserRouter.get_users")
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 5


@pytest.mark.anyio
async def test_get_user(
    fastapi_app: FastAPI,
    client: AsyncClient,
    user_manager: UserManager,
) -> None:
    """Tests dummy instance creation."""
    user = await user_manager.add_user(
        user=CreateUserRequest(
            email="admin@gmail.com",
            phone="123456",
        ),
    )
    url = fastapi_app.url_path_for("UserRouter.by_id")
    response = await client.get(url, params=QueryParams(user_id=user.id))
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == str(user.id)


@pytest.mark.anyio
async def test_remove_user(
    fastapi_app: FastAPI,
    client: AsyncClient,
    user_manager: UserManager,
) -> None:
    """Tests dummy instance creation."""
    user = await user_manager.add_user(
        user=CreateUserRequest(
            email="admin@gmail.com",
            phone="123456",
        ),
    )

    url = fastapi_app.url_path_for("UserRouter.remove_user")
    response = await client.delete(url, params=QueryParams(user_id=user.id))
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == str(user.id)
    assert data["msg"] == "Deleted user successfully"
