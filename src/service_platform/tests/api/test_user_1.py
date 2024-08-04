
import unittest
from service_platform.db.user.table import UserEntity
from service_platform.tests.api.test_base import BaseTest
from service_platform.tests.client.user import UserClient

class TestUser(BaseTest):    
    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.userClient = UserClient(await self.client(self.api))


    async def test_get_user_info(self) -> None:
        user: UserEntity = await self.create_user(self.user_repository)
        token: str = await self.access_token(user)
        response = await self.userClient.me(token)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["email"], user.email)
    
    async def test_get_user_info_fail(self) -> None:
        response = await self.userClient.me("123")
        
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()