import pytest
from faker import Faker
from fastapi import FastAPI
from httpx import AsyncClient, QueryParams
from starlette import status

from service_platform_py.api.router.user.manager import UserManager
from service_platform_py.api.router.user.schema import CreateUserRequest

faker = Faker()

# async def test_user_sample(
#     api: FastAPI
# ) -> None:
#     url = api.url_path_for("UserRouter.new")
#     print(url)
#     client = UserClient(base_url=url)
#     response = await client.sample()
#     print(response)


@pytest.mark.anyio
async def test_user_creation(
    api: FastAPI,
    client: AsyncClient,
    user_manager: UserManager,
) -> None:
    """Tests dummy instance creation."""
    url = api.url_path_for("UserRouter.new")
    email = faker.email()
    response = await client.post(
        url,
        json={
            "email": email,
            "phone": faker.phone_number(),
        },
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    instances = await user_manager.by_id(data["id"])
    assert instances.email == email

    instances = await user_manager.by_email(email)
    assert instances.email == email


@pytest.mark.anyio
async def test_get_users(
    api: FastAPI,
    client: AsyncClient,
    user_manager: UserManager,
) -> None:
    """Tests dummy instance creation."""
    for i in range(5):
        await user_manager.add_user(
            user=CreateUserRequest(
                email=faker.email(),
                phone=faker.phone_number(),
            ),
        )
    url = api.url_path_for("UserRouter.get_users")
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 5


@pytest.mark.anyio
async def test_get_user(
    api: FastAPI,
    client: AsyncClient,
    user_manager: UserManager,
) -> None:
    """Tests dummy instance creation."""
    email = faker.email()
    user = await user_manager.add_user(
        user=CreateUserRequest(
            email=email,
            phone=faker.phone_number(),
        ),
    )
    url = api.url_path_for("UserRouter.by_id")
    response = await client.get(url, params=QueryParams(user_id=user.id))
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == str(user.id)


@pytest.mark.anyio
async def test_remove_user(
    api: FastAPI,
    client: AsyncClient,
    user_manager: UserManager,
) -> None:
    """Tests dummy instance creation."""
    email = faker.email()
    user = await user_manager.add_user(
        user=CreateUserRequest(
            email=email,
            phone=faker.phone_number(),
        ),
    )

    url = api.url_path_for("UserRouter.remove_user")
    response = await client.delete(url, params=QueryParams(user_id=user.id))
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == str(user.id)
    assert data["msg"] == "Deleted user successfully"
