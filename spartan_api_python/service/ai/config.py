from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel

from spartan_api_python.settings import settings


@dataclass
class PineconeConfig:
    api_key: str
    index_name: str
    environment: str

    @property
    def dict(self) -> dict[str, Optional[str]]:
        return {
            "api_key": self.api_key,
            "environment": self.environment,
        }


@dataclass
class OpenAIConfig:
    api_key: str


class PipelineConfig(BaseModel):
    """Configuration settings for the pipeline."""

    pinecone_index_name: str = settings.pinecone_index_name
    pinecone_environment: Optional[str] = settings.pinecone_environment
    pinecone_api_key: Optional[str] = settings.pinecone_api_key
    openai_api_key: Optional[str] = settings.openai_api_key

    @property
    def open_ai(self) -> OpenAIConfig:
        return OpenAIConfig(api_key=self.openai_api_key)

    @property
    def pinecone(self) -> PineconeConfig:
        return PineconeConfig(
            api_key=self.pinecone_api_key,
            index_name=self.pinecone_index_name,
            environment=self.pinecone_environment,
        )
