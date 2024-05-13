from service_platform_py.core.repository.repository_base import BaseRepository
from service_platform_py.db.user.table import UserEntity


class UserRepository(BaseRepository[UserEntity]):
    entity = UserEntity
