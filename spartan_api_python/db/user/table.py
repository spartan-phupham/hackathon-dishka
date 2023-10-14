from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import TIMESTAMP

from spartan_api_python.db.base import BaseTable


class UserTable(BaseTable):
    __tablename__ = "users"
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=True)
    status = Column(String, unique=True, nullable=True)
    level = Column(String, unique=True, nullable=False)
    logged_in_at = Column(TIMESTAMP(timezone=True), default=None)
