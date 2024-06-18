from sqlalchemy import Column, UUID, func

from service_platform.db.base_table import BaseTable


class RefreshTokenEntity(BaseTable):
    __tablename__ = "refresh_tokens"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4()
    )

    user_id = Column(UUID(as_uuid=True), nullable=False)
