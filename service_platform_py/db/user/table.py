from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import TIMESTAMP

from service_platform_py.db.base_table import BaseTable


class UserEntity(BaseTable):
    __tablename__ = "users"
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=True)
    status = Column(String, nullable=False)
    level = Column(String, nullable=False)
    logged_in_at = Column(TIMESTAMP(timezone=True), default=None)
