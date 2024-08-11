
from dataclasses import asdict
import unittest
from service_platform.client.model.auth_provider import AuthProvider
from service_platform.db.user.table import UserEntity
from service_platform.tests.client.user import UserClient
from service_platform.tests.repository.test_base import TestBase
from faker import Faker

fake = Faker()

class TestUser(TestBase):    
    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.user = UserEntity(
            auth_id=fake.uuid4(),
            email=fake.email(),
            name=fake.user_name(),
            picture_url=fake.image_url(),
            auth_provider=AuthProvider.GOOGLE,
        )
        

    async def asyncTearDown(self):
        await super().asyncTearDown()

    async def createUser(self, user: UserEntity) -> UserEntity:
        return await self.user_repository.insert_user(
            auth_id=user.auth_id,
            email=user.email,
            name=user.name,
            picture_url=user.picture_url,
            auth_provider=user.auth_provider
        )

    async def test_create_user(self):
        user: UserEntity = await self.createUser(self.user)
        assert user.auth_id == self.user.auth_id
        assert user.email == self.user.email
        assert user.name == self.user.name
        assert user.picture_url == self.user.picture_url

if __name__ == "__main__":
    unittest.main()