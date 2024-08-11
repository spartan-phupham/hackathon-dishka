import unittest
from service_platform.tests.api.test_base import TestBase
from service_platform.tests.client.health import HealthClient

class TestHealth(TestBase):    
    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.healthClient = HealthClient(await self.client(self.api))
    
    async def asyncTearDown(self):
        await super().asyncTearDown()

    async def test_health(self) -> None:
        response = await self.healthClient.health()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "OK")

if __name__ == "__main__":
    unittest.main()