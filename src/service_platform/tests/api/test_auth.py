
import unittest
from unittest.mock import AsyncMock, patch
from faker import Faker
from parameterized import parameterized
from service_platform.client.response.auth.auth_response import LoginResponse
from service_platform.db.user.table import UserEntity
from service_platform.exception.auth_error import AuthError
from service_platform.settings import settings
from service_platform.tests.api.test_base import TestBase
from service_platform.tests.client.auth import AuthClient

fake = Faker()

class AuthTest(TestBase): 
    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.authClient = AuthClient(await self.client(self.api))
        self.user: UserEntity = await self.create_user(self.user_repository)
        self.refresh_token = await self.refresh_token(self.token_generator, self.user)

    async def asyncTearDown(self):
        await super().asyncTearDown()
        await self.authClient.client.aclose()

    @parameterized.expand(["google", "linkedin"])
    async def test_provider_login(self, provider):
        payload = {"code": "test_authorization_code"}

        token_info_mock = AsyncMock()
        token_info_mock.access_token = fake.random_letters()

        user_info_mock = AsyncMock()
        user_info_mock.id = fake.uuid4()
        user_info_mock.email = fake.email()
        user_info_mock.name = fake.name()
        user_info_mock.picture_url = fake.image_url()


        with patch(
            f"service_platform.service.{provider}.oauth"
            f".{provider.capitalize()}OAuthService.exchange_code_for_token",
            return_value=token_info_mock,
        ):
            with patch(
                f"service_platform.service.{provider}.oauth"
                f".{provider.capitalize()}OAuthService.get_user_info",
                return_value=user_info_mock,
            ):
                response = await self.authClient.provider_authorize_login(provider=provider, payload=payload)
                assert response.status_code == 200

                login_response = LoginResponse(**response.json())
                assert login_response.expires_in == settings.jwt.expiration_time

    @parameterized.expand(["google", "linkedin"])
    async def test_provider_login_incredential(self, provider):
        payload = {"code": "test_in_authorization_code"}

        with patch(
            f"service_platform.service.{provider}.oauth"
            f".{provider.capitalize()}OAuthService.exchange_code_for_token",
            return_value=None,
        ):
            with patch(
                f"service_platform.service.{provider}.oauth"
                f".{provider.capitalize()}OAuthService.get_user_info",
                return_value=None,
            ):
                response = await self.authClient.provider_authorize_login(provider=provider, payload=payload)
                assert (
                    response.status_code == AuthError.INVALID_CREDENTIALS.as_http_exception().status_code
                )
                messages = response.json()["messages"]
                assert AuthError.INVALID_CREDENTIALS.message in messages
    
    async def test_refresh_token(self):
        response = await self.authClient.refresh_token(token=self.refresh_token)
        assert response.status_code == 200

        login_response = LoginResponse(**response.json())
        assert login_response.expires_in == settings.jwt.expiration_time

    
    
    async def test_logout(self):
        refresh_token_response = await self.authClient.refresh_token(token=self.refresh_token)
        assert refresh_token_response.status_code == 200

        logout_response = await self.authClient.logout(self.refresh_token)
        assert logout_response.status_code == 200

        after_logged_out_response = await self.authClient.refresh_token(self.refresh_token)
        assert after_logged_out_response.status_code == 401

if __name__ == "__main__":
    unittest.main()