import base64
import uuid

import jwt
from fastapi import HTTPException

from service_platform.core.middleware.model import TokenType
from service_platform.core.security.model import TokenData
from service_platform.core.security.token_validator import TokenValidator
from service_platform.settings import settings, logger


class JwtTokenValidator(TokenValidator):
    def __init__(self):
        self.public_key = base64.b64decode(settings.jwt.public_key_base64)
        self.algorithm = settings.jwt.algorithm
        self.issuer = settings.jwt.issuer

    async def validate(self, token: str, token_type: TokenType) -> TokenData:
        try:
            payload = jwt.decode(
                token,
                self.public_key,
                algorithms=[self.algorithm],
                issuer=self.issuer,
            )
            if payload.get("type") != token_type.value:
                raise HTTPException(
                    status_code=401,
                    detail="Token is invalid or has expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            user_id: str = payload.get("sub")
            if user_id is None:
                raise HTTPException(
                    status_code=401,
                    detail="Token does not contain user ID (sub).",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            roles: list[str] = payload.get("roles", [])
            jti: str = payload.get("jti", None)
            return TokenData(user_id=uuid.UUID(user_id), roles=roles, jti=jti)
        except Exception as e:
            logger.error(f"Error validating token: {e}")
            raise HTTPException(
                status_code=401,
                detail="Token is invalid or has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
