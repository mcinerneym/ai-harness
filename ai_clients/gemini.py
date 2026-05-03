from typing import List
from .client_interface import LlmClientInterface
from .message import Message
import logging

from config.clients import gemini_client

class _GeminiClient(LlmClientInterface):
    def __init__(self):
        self._client = gemini_client
        self._models = self._client.models.list().page
        self._model_name = "gemma-4-31b-it"
        self._context: List[Message] = []
        self._usage = 0
    
    def get_models(self) -> List[str]:
        return self.models
    
    def select_model(self, model_name: str) -> None:
        return ""
    
    def call_llm(self, query: str) -> str:
        self._context.append(Message(role = "user", text = query))
        response = self._client.models.generate_content(
            model = self._model_name, contents = f"{self._context}"
        )
        response_text = response.text
        self._context.append(Message(
            role = "llm", 
            text = response_text)
        )
        self._usage += response.usage_metadata.total_token_count
        return response_text
    
    def get_usage(self) -> int:
        return self._usage
    
    def get_context_size(self) -> int:
        if self._context == []:
            return "0"
        full_context_string = f"{self._context}"
        response = self._client.models.count_tokens(
            model = self._model_name,
            contents = full_context_string
        )
        return response.total_tokens

    def close(self) -> None:
        self._client.close()


gemini_class = _GeminiClient()