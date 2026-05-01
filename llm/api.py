from config.gemini import gemini_client

def call_llm(query: str) -> str:
    response = gemini_client.models.generate_content(
        model = "gemma-4-31b", contents = query
    )
    return response.text