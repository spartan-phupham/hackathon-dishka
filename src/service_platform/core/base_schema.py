import uuid
from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import BaseModel


def convert_datetime_to_gmt(dt: datetime) -> str:
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))

    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")


class CoreModel(BaseModel):
    class Config:
        json_encoders = {datetime: convert_datetime_to_gmt}
        populate_by_name = True
        from_attributes = False


class OrmModel(CoreModel):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime | None
    deleted_at: datetime | None

    class Config(CoreModel.Config):
        from_attributes = True
