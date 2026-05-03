from typing import TypedDict

class Message(TypedDict):
    role: str
    user_query: str
    llm_response: str