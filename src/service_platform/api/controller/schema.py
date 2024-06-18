"""spartan_api_python API package."""

from pydantic import BaseModel


class MessageResponse(BaseModel):
    """Simple message model."""

    message: str
