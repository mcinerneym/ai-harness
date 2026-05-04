
from .gemini import gemini_class
from .client_interface import LlmClientInterface
from typing import Dict

class LlmClientFactory():

    def __init__(self):
        self._client_registry: Dict[str, LlmClientInterface]
        models = gemini_class.get_models()
        for model in models:
            self._client_registry[model] = gemini_class

    def get_client(self, model_name: str) -> LlmClientInterface:
        if model_name not in self._client_registry:
            raise Exception(f"{model_name} not found")
        return self._client_registry[model_name]