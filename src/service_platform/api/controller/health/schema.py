from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Simple message model."""

    message: str
