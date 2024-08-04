import uuid

from service_platform.api.manager.user.response import UserResponseConverter
from service_platform.client.response.user.user_response import UserResponse
from service_platform.db.user.repository import UserRepository


class UserManager:
    def __init__(
        self,
        user_repository: UserRepository,
        user_response_converter: UserResponseConverter,
    ):
        self.user_repository = user_repository
        self.user_response_converter = user_response_converter

    async def me(self, user_id: uuid.UUID) -> UserResponse:
        user = await self.user_repository.get(user_id)
        return self.user_response_converter.to_user_response(user)
