from typing import List
from .client_interface import LlmClientInterface
import logging

from config.clients import gemini_client

class _GeminiClient(LlmClientInterface):
    def __init__(self):
        self._client = gemini_client
        self._models = self._client.models.list().page
    
    def get_models(self) -> List[str]:
        model_names = []
        for model in self._models:
            model_names.append(str.split(model.name, "/")[-1])
        return model_names
    
    
    def call_llm(self, query: str, model_name: str) -> tuple[str, int]:
        response = self._client.models.generate_content(
            model = model_name, contents = query
        )
        response_text = response.text
        usage = response.usage_metadata.total_token_count
        return response_text, usage
    
    def call_llm_stream(self, query: str, model_name: str):
        try:
            response = self._client.models.generate_content_stream(
                model=model_name,
                contents=query
            )
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            raise e
    
    def get_context_size(self, context: str, model_name: str) -> int:
        response = self._client.models.count_tokens(
            model = model_name,
            contents = context
        )
        return response.total_tokens

    def close(self) -> None:
        self._client.close()


gemini_class = _GeminiClient()