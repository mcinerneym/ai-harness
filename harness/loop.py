from typing import List
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.markdown import Markdown
from rich.layout import Layout
from ai_clients.gemini import gemini_class
from ai_clients.client_interface import LlmClientInterface
from commands.registry import check_command, execute_command
from commands.system import *
from commands.llm import *
from config.rich_format import *
from agents.main_agent import Agent

def llm_loop():
    client: LlmClientInterface = gemini_class
    agent: Agent = Agent(client)
    console = Console()
    console.print(Panel(Markdown("# Welcome to the Harness"), border_style=SYSTEM_CONSOLE_COLOR))
    while True:
        query = console.input("> ")
        if check_command(query.lower()):
            command_response = execute_command(query.lower(), agent)
            console.print(Panel(Markdown(command_response), border_style=SYSTEM_CONSOLE_COLOR))
        else:
            try:
                with Live(Panel("", title="Agent", border_style=MODEL_CONSOLE_COLOR)) as live:
                    partial = ""
                    for chunk in agent.call_llm_stream(query):
                        partial += chunk
                        live.update(Panel(Markdown(partial), title="Agent", border_style=MODEL_CONSOLE_COLOR))
            except Exception as e:
                console.print(Panel(Markdown(f"Error with the model: {e}"), title="System", border_style=ERROR_CONSOLE_COLOR))