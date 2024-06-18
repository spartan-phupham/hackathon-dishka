class CustomAuthentication:
    user_id: str
    roles: list[str]

    def __init__(self, user_id: str, roles: list[str], jti: str | None = None):
        self.user_id = user_id
        self.roles = roles
        self.jti = jti

    def dict(self):
        return {
            "sub": self.user_id,
            "roles": self.roles,
            "jti": self.jti,
        }
