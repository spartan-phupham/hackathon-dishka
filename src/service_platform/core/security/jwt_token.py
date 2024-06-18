class JWTToken:
    def __init__(
        self,
        access_token: str,
        refresh_token: str = None,
        expires_in: int = 1440,
        token_type: str = "Bearer",
    ):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_in = expires_in
        self.token_type = token_type
