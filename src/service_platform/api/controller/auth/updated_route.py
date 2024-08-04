from typing import Annotated
from fastapi import APIRouter, Depends

from service_platform.api.controller.schema import MessageResponse
from service_platform.client.model.auth_provider import AuthProvider
from service_platform.api.manager.auth.manager import AuthManager
from service_platform.client.request.auth.auth_request import ProviderLoginRequest
from service_platform.client.response.auth.auth_response import LoginResponse
from service_platform.core.middleware.authentication import get_token_data, public_endpoint, refresh_token_endpoint

from dishka.integrations.fastapi import FromDishka, inject

from service_platform.core.security.model import TokenData


router = APIRouter()

@router.get("/login/{provider}")
@public_endpoint
@inject
async def get_provider_redirect_url(
    self, 
    provider: AuthProvider,
    manager: FromDishka[AuthManager]
) -> MessageResponse:
    return await self.manager.get_provider_redirect_url(provider=provider)

@router.post("/login/{provider}")
@public_endpoint
@inject
async def provider_authorize_login(
    self, 
    payload: ProviderLoginRequest, 
    provider: AuthProvider
) -> LoginResponse:
    return await self.manager.provider_authorize_login(
        payload=payload, provider=provider
    )

@router.post("/refresh-token")
@refresh_token_endpoint
async def refresh_token(
    self,
    token_data: Annotated[TokenData, Depends(get_token_data)],
    manager: FromDishka[AuthManager]
) -> LoginResponse:
    return await manager.refresh_access_token(
        user_id=token_data.user_id, jti=token_data.jti
    )

@router.post("/logout")
@refresh_token_endpoint
async def logout(
    self,
    token_data: Annotated[TokenData, Depends(get_token_data)],
    manager: FromDishka[AuthManager]
) -> MessageResponse:
    return await manager.logout(user_id=token_data.user_id, jti=token_data.jti)