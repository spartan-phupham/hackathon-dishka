from httpx import AsyncClient

from service_platform.tests.client.base import BaseClient

class UserClient(BaseClient):
    def __init__(self, client: AsyncClient):
        self.client = client

    async def me(self, token: str):
        url = "/api/user/me"
        return await self.modify_authoriztion_header(
            client=self.client, 
            token=token
        ).get(url)