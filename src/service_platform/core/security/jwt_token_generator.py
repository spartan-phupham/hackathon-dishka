import base64

import jwt
from fastapi import Depends

from service_platform.core.middleware.model import TokenType
from service_platform.core.security.custom_authentication import CustomAuthentication
from service_platform.core.security.jwt_claim_generator import JWTClaimGenerator
from service_platform.core.security.jwt_token import JWTToken
from service_platform.core.security.token_generator import TokenGenerator
from service_platform.settings import settings


class JWTTokenGenerator(TokenGenerator):
    def __init__(self, claim_generator: JWTClaimGenerator = Depends()):
        self.claim_generator = claim_generator
        self.secret_key = base64.b64decode(settings.jwt.secret_key_base64)
        self.algorithm = settings.jwt.algorithm
        self.expiration_time = settings.jwt.expiration_time
        self.refresh_expiration_time = settings.jwt.refresh_expiration_time

    def generate_token(
        self, authentication: CustomAuthentication, generate_refresh_token: bool = True
    ) -> JWTToken:
        access_token = jwt.encode(
            self.claim_generator.generate_claims(
                token_type=TokenType.access_token,
                data=authentication.dict(),
                expires_in=self.expiration_time,
            ),
            self.secret_key,
            algorithm=self.algorithm,
        )
        refresh_token = None
        if generate_refresh_token is True:
            refresh_token = jwt.encode(
                self.claim_generator.generate_claims(
                    token_type=TokenType.refresh_token,
                    data=authentication.dict(),
                    expires_in=self.refresh_expiration_time,
                ),
                self.secret_key,
                algorithm=self.algorithm,
            )

        return JWTToken(access_token, refresh_token, self.expiration_time)
