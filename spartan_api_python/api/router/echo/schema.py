from pydantic import BaseModel


class EchoRequest(BaseModel):
    """Simple message model."""

    message: str


class EchoResponse(BaseModel):
    """Simple message model."""

    message: str
