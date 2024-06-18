from unittest.mock import AsyncMock, patch

import pytest
from faker import Faker
from fastapi import FastAPI
from httpx import AsyncClient
from service_platform.client.response.auth.auth_response import LoginResponse
from service_platform.exception.auth_error import AuthError
from service_platform.settings import settings

fake = Faker()


@pytest.mark.anyio
@pytest.mark.parametrize("provider", ["google", "linkedin"])
async def test_provider_login(client: AsyncClient, api: FastAPI, provider: str) -> None:
    url = api.url_path_for("AuthRouter.provider_authorize_login", provider=provider)
    payload = {"code": "test_authorization_code"}

    user_info_mock = AsyncMock()
    user_info_mock.id = fake.uuid4()
    user_info_mock.email = fake.email()
    user_info_mock.name = fake.name()
    user_info_mock.picture_url = fake.image_url()

    token_info_mock = AsyncMock()
    token_info_mock.access_token = fake.random_letters()

    with patch(
        f"service_platform.service.{provider}.dependency"
        f".{provider.capitalize()}Service.exchange_code_for_token",
        return_value=token_info_mock,
    ):
        with patch(
            f"service_platform.service.{provider}.dependency"
            f".{provider.capitalize()}Service.get_user_info",
            return_value=user_info_mock,
        ):
            response = await client.post(url, json=payload)
            assert response.status_code == 200

            login_response = LoginResponse(**response.json())
            assert login_response.expires_in == settings.jwt.expiration_time


@pytest.mark.anyio
@pytest.mark.parametrize("provider", ["google", "linkedin"])
async def test_provider_login_incredential(
    client: AsyncClient, api: FastAPI, provider: str
) -> None:
    url = api.url_path_for("AuthRouter.provider_authorize_login", provider=provider)
    payload = {"code": "test_in_authorization_code"}

    with patch(
        f"service_platform.service.{provider}.dependency"
        f".{provider.capitalize()}Service.exchange_code_for_token",
        return_value=None,
    ):
        with patch(
            f"service_platform.service.{provider}.dependency"
            f".{provider.capitalize()}Service.get_user_info",
            return_value=None,
        ):
            response = await client.post(url, json=payload)
            assert (
                response.status_code
                == AuthError.INVALID_CREDENTIALS.as_http_exception().status_code
            )
            messages = response.json()["messages"]
            assert AuthError.INVALID_CREDENTIALS.message in messages


@pytest.mark.anyio
async def test_refresh_token(
    authenticated_client_with_refresh_token: AsyncClient, api: FastAPI
) -> None:
    url = api.url_path_for("AuthRouter.refresh_token")

    response = await authenticated_client_with_refresh_token.post(url)
    assert response.status_code == 200

    login_response = LoginResponse(**response.json())
    assert login_response.expires_in == settings.jwt.expiration_time


@pytest.mark.anyio
async def test_logout(
    authenticated_client_with_refresh_token: AsyncClient, api: FastAPI
) -> None:
    refresh_token_url = api.url_path_for("AuthRouter.refresh_token")
    logout_url = api.url_path_for("AuthRouter.logout")

    refresh_token_response = await authenticated_client_with_refresh_token.post(
        refresh_token_url
    )
    assert refresh_token_response.status_code == 200

    logout_response = await authenticated_client_with_refresh_token.post(logout_url)
    assert logout_response.status_code == 200

    after_logged_out_response = await authenticated_client_with_refresh_token.post(
        refresh_token_url
    )
    assert after_logged_out_response.status_code == 401
