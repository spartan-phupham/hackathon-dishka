from httpx import AsyncClient

from service_platform.client.request.auth.auth_request import ProviderLoginRequest
from service_platform.tests.client.base import BaseClient

class AuthClient(BaseClient):
    def __init__(self, client: AsyncClient):
        self.client = client

    async def get_provider_redirect_url(self, provider: str):
        url = f"/api/auth/login/{provider}"
        return await self.client.get(url)
    
    async def provider_authorize_login(self, provider: str, payload: str):
        url = f"/api/auth/login/{provider}"
        return await self.client.post(url, json=payload)
    
    async def refresh_token(self, token: str):
        url = f"/api/auth/refresh-token"
        return await self.modify_authoriztion_header(
            client=self.client,
            token=token
        ).post(url)
    
    async def logout(self, token: str):
        url = "/api/auth/logout"
        return await self.modify_authoriztion_header(
            client=self.client,
            token=token
        ).post(url)