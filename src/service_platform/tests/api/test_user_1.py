
import unittest
from faker import Faker
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)
from service_platform.client.model.auth_provider import AuthProvider
from service_platform.core.security.custom_authentication import CustomAuthentication
from service_platform.core.security.jwt_claim_generator import JWTClaimGenerator
from service_platform.core.security.jwt_registered_claim import JWTRegisteredClaim
from service_platform.core.security.jwt_token_generator import JWTTokenGenerator
from service_platform.db.user.repository import UserRepository
from service_platform.db.user.table import UserEntity
from service_platform.tests.api.test_base import BaseTestClass
from service_platform.tests.conftest import DEFAULT_USER_EMAIL

fake = Faker()
DEFAULT_USER_NAME = fake.user_name()
DEFAULT_USER_EMAIL = fake.email()
DEFAULT_USER_ID = fake.uuid4()
DEFAULT_USER_PICTURE = fake.image_url()

class TestUserInfo(BaseTestClass):
    def claim_generator(self) -> JWTClaimGenerator:
        return JWTClaimGenerator(
            registered_claim=JWTRegisteredClaim(),
        )


    def token_generator(
        self,
        claim_generator: JWTClaimGenerator,
    ) -> JWTTokenGenerator:
        return JWTTokenGenerator(
            claim_generator=claim_generator,
        )
    
    async def access_token(
        self,
        test_user: UserEntity,
        token_generator: JWTTokenGenerator,
    ) -> str:
        """
        Fixture to create an access token for the test user.
        """
        authentication = CustomAuthentication(
            user_id=str(test_user.id),
            roles=[test_user.roles],
        )
        jwt_token = token_generator.generate_token(authentication)
        return jwt_token.access_token
    
    async def authenticated_client(self, client: AsyncClient, access_token: str) -> AsyncClient:
        """
        Fixture to create an authenticated client.
        """
        client.headers = {
            **client.headers,
            "Authorization": f"Bearer {access_token}",
        }
        return client
    
    def user_repository(
        self,
        dbsession: AsyncSession,
    ) -> UserRepository:
        return UserRepository(dbsession)

    async def user(
        self,
        user_repository: UserRepository,
    ) -> UserEntity:
        return await user_repository.insert_user(
            auth_id=DEFAULT_USER_ID,
            email=DEFAULT_USER_EMAIL,
            name=DEFAULT_USER_NAME,
            picture_url=DEFAULT_USER_ID,
            auth_provider=AuthProvider.GOOGLE,
        )
    
    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.user_repository = self.user_repository(self.session)
        self.claim_generator = self.claim_generator()
        self.token_generator = self.token_generator(self.claim_generator)


    async def test_get_user_info(self) -> None:
        url = "/user/me"
        user: UserEntity = await self.user(self.user_repository)
        token: str = await self.access_token(user, self.token_generator)
        print(token)
        client: AsyncClient = await self.authenticated_client(self.client, token)
        print(client.headers)
        response = await client.get(url)
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["email"], DEFAULT_USER_EMAIL)

if __name__ == "__main__":
    unittest.main()