from httpx import AsyncClient

from service_platform.tests.client.base import BaseClient

class HealthClient(BaseClient):
    def __init__(self, client: AsyncClient):
        self.client = client


    async def health(self):
        url = "/api/health/"
        return await self.client.get(url)