from abc import ABC, abstractmethod
from typing import List

class LlmClientInterface(ABC):
    
    @abstractmethod
    def call_llm(self) -> str:
        pass

    @abstractmethod
    def get_models(self) -> List[str]:
        pass

    @abstractmethod
    def select_model(self, model_name: str):
        pass

    @abstractmethod
    def get_usage(self) -> int:
        pass

    @abstractmethod
    def close(self) -> None:
        pass