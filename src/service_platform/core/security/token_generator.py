from abc import ABC, abstractmethod
from typing import Any


class TokenGenerator(ABC):
    @abstractmethod
    def generate_token(self, data: dict) -> Any:
        pass


class ClaimGenerator(ABC):
    @abstractmethod
    def generate_claims(self, token_type: str, data: dict) -> dict:
        pass
