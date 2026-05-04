from .registry import harness_command
from agents.main_agent import Agent
from config.markdown_format import *

@harness_command("exit", "Exit the program")
def exit_harness(client: Agent) -> str:
    exit(0)
    client.close_client()
    return ""

@harness_command("usage", "Get the tokens this Agent has used")
def get_usage(client: Agent) -> str:
    usage = client.get_usage()
    return f"Current Usage: {bold(f"{usage}" + " tokens")}"

@harness_command("context", "Get the current context being used by the Agent")
def get_context_size(client: Agent) -> str:
    context_size = client.get_context_size()
    return f"Current Context Size: {bold(f"{context_size}" + " tokens")}"