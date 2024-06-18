from sqlalchemy import Column, UUID, func, Text, String
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship

from service_platform.db.base_table import BaseTable


class UserEntity(BaseTable):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )
    email = Column(Text, nullable=False)
    name = Column(Text)
    picture_url = Column(Text)
    logged_in_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    roles: str = Column(String, nullable=True)
    auth_id: str = Column(String, nullable=True)
    auth_provider: str = Column(String, nullable=False)
