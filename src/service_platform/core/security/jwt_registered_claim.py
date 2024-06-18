from service_platform.settings import settings


class JWTRegisteredClaim:
    def __init__(self):
        self.issuer = settings.jwt.issuer
        self.expiration_time = settings.jwt.expiration_time
