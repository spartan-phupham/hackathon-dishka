import uuid

from fastapi import APIRouter

from spartan_api_python.api.router.user.schema import UserResponse
from spartan_api_python.db.user.repository import UserRepository
from spartan_api_python.db.user.table import UserEntity


class UserRouter:
    def __init__(
        self,
        router: APIRouter,
        repository: UserRepository
    ):
        super().__init__()
        self.router = router
        self.repository = repository
        self.router.add_api_route("/home", self.home, methods=["GET"])
        self.router.add_api_route("/by-id", self.by_id, methods=["GET"])

    @staticmethod
    async def home() -> UserResponse:
        return UserResponse(
            id=uuid.UUID("00000000-0000-0000-0000-000000000000"),
            phone="+1234567890",
            email="chan@c0x12c.com",
            status="active",
            level="admin"
        )

    async def by_id(self, id: str) -> UserResponse:
        user: UserEntity = self.repository.by_id(id)
        if user is None:
            raise ValueError("User not found")
        return UserResponse(
            phone=user.phone,
            email=user.email,
            status=user.status,
            level=user.level
        )
