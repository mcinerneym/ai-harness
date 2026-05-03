from typing import List
from .client_interface import LlmClientInterface
from .message import Message

from config.clients import gemini_client

class _GeminiClient(LlmClientInterface):
    def __init__(self):
        self._client = gemini_client
        self._models = self._client.models.list().page
        self._model = "gemma-4-31b-it"
        self._context: List[Message] = []
    
    def get_models(self) -> List[str]:
        return self.models
    
    def select_model(self, model_name: str) -> None:
        return ""
    
    def call_llm(self, query: str) -> str:
        final_query = f"[latest_query: {query}], history: {self._context}"
        response = self._client.models.generate_content(
            model = self._model, contents = final_query
        )
        response_text = response.text
        self._context.append(Message(
            role = "basic", 
            user_query = query, 
            llm_response = response_text)
        )
        return response.text
    
    # TODO
    def get_usage(self) -> None:
        pass

    def close(self) -> None:
        self._client.close()


gemini_class = _GeminiClient()