import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status


@pytest.mark.anyio
async def test_health(
    client: AsyncClient,
    api: FastAPI,
) -> None:
    """
    Checks the health endpoint.

    :param client: client for the app.
    :param api: current FastAPI application.
    """
    url = api.url_path_for("HealthRouter.health")
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK
