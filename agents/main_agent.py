from ai_clients.client_interface import LlmClientInterface
from .message import Message
from typing import List

class Agent:

    def __init__(self, client: LlmClientInterface, context: List[Message] = [], usage: int = 0 ):
        self._client = client
        self._model = "gemma-4-31b-it"
        self._context: List[Message] = context
        self._usage = usage

    def call_llm(self, query: str, role: str="user") -> str:
        self._context.append(Message(role = role, text = query))
        response, usage = self._client.call_llm(f"{self._context}", self._model)
        self._context.append(Message(
            role = "llm", 
            text = response)
        )
        self._usage += usage
        return response
    
    def call_llm_stream(self, query: str, role: str="user") -> str:
        self._context.append(Message(role = role, text = query))
        all_text = ""

        try:
            for response_chunk in self._client.call_llm_stream(f"{self._context}", self._model):
                all_text += response_chunk
                yield response_chunk
        
            self._context.append(Message(
                role = "llm", 
                text = all_text)
            )
        except Exception as e:
            raise e
    
    def get_usage(self) -> int:
        return self._usage
    
    def get_context_size(self) -> int:
        if not self._context:
            return 0
        return self._client.get_context_size(f"{self._context}", self._model)
    
    def change_model_and_client(self, model_name: str, client: LlmClientInterface) -> None:
        self._client = client
        self._model = model_name
    
    def close_client(self) -> None:
        self._client.close()

    def clear_current_context(self) -> None:
        self._context = []
        