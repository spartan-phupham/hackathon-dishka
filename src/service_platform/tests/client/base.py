from httpx import AsyncClient

class BaseClient: 
    def modify_authoriztion_header(self, client: AsyncClient, token: str = None) -> AsyncClient:
        if token != None:
            self.client.headers = {
                **self.client.headers,
                "Authorization": f"Bearer {token}"
            }
        return client