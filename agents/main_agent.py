from ai_clients.client_interface import LlmClientInterface
from .message import Message
from typing import List

class Agent:

    def __init__(self, client: LlmClientInterface, context: List[Message] = [], usage: int = 0 ):
        self._client = client
        self._model = "gemma-4-31b-it"
        self._context: List[Message] = context
        self._usage = usage

    def call_llm(self, query: str) -> str:
        self._context.append(Message(role = "user", text = query))
        response, usage = self._client.call_llm(f"{self._context}", self._model)
        self._context.append(Message(
            role = "llm", 
            text = response)
        )
        self._usage += usage
        return response
    
    def get_usage(self) -> int:
        return self._usage
    
    def get_context_size(self) -> int:
        if not self._context:
            return 0
        return self._client.get_context_size(f"{self._context}")
    
    def close_client(self) -> None:
        self._client.close()
        