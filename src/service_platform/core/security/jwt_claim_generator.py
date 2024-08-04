from datetime import timedelta, datetime, UTC

from service_platform.core.middleware.model import TokenType
from service_platform.core.security.jwt_registered_claim import JWTRegisteredClaim
from service_platform.core.security.token_generator import ClaimGenerator


class JWTClaimGenerator(ClaimGenerator):
    def __init__(self, registered_claim: JWTRegisteredClaim):
        self.registered_claim = registered_claim

    def generate_claims(
        self,
        token_type: TokenType,
        data: dict,
        expires_in: int | None = None,
        jti: str = None,
    ) -> dict:
        claims = {
            "jti": jti,
            "type": token_type.value,
            "iss": self.registered_claim.issuer,
            "iat": datetime.now(UTC),
            "nbf": datetime.now(UTC),
            **data,
        }
        if expires_in != -1:
            expires_in = datetime.now(UTC) + timedelta(
                seconds=expires_in or self.registered_claim.expiration_time
            )
            claims["exp"] = expires_in

        return claims
