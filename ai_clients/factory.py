
from .gemini import gemini_class
from .client_interface import LlmClientInterface
from typing import Dict, List

client_list: List[LlmClientInterface] = [gemini_class]

class LlmClientFactory():
    def __init__(self):
        self._client_registry: Dict[str, LlmClientInterface] = {}
        for client in client_list:
            models = client.get_models()
            for model in models:
               self._client_registry[model] = client

    def get_client(self, model_name: str) -> LlmClientInterface:
        if model_name not in self._client_registry:
            raise Exception(f"{model_name} not found")
        return self._client_registry[model_name]
    
    def list_model_names(self) -> List[str]:
        return list(self._client_registry.keys())
    

llmClientFactory = LlmClientFactory()