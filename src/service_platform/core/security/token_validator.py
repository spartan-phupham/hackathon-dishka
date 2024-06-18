from abc import ABC, abstractmethod
from typing import Any

from service_platform.core.middleware.model import TokenType


class TokenValidator(ABC):
    @abstractmethod
    def validate(self, token: str, token_type: TokenType) -> Any:
        pass
