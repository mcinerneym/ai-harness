from typing import List
from rich.console import Console
from rich.panel import Panel
from ai_clients.gemini import gemini_class
from ai_clients.client_interface import LlmClientInterface

def llm_loop():
    client: LlmClientInterface = gemini_class
    console = Console()
    console.print(Panel("Hello, Welcome to the Harness", border_style="green"))
    while True:
        query = console.input("> ")
        if query == "exit":
            console.print(Panel("Exiting...", border_style="green"))
            exit(0)
        
        response = client.call_llm(query)
        console.print(Panel(response, title="Agent", border_style="blue"))