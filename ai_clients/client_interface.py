from abc import ABC, abstractmethod
from typing import List

class LlmClientInterface(ABC):
    
    @abstractmethod
    def call_llm(self, query: str, model_name: str) -> tuple[str, int]:
        pass

    @abstractmethod
    def get_models(self) -> List[str]:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

    @abstractmethod
    def get_context_size(self, context: str, model_name: str) -> int:
        pass