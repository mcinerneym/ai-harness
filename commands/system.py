from .registry import harness_command
from agents.main_agent import Agent
from config.markdown_format import *
from ai_clients.factory import llmClientFactory

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

@harness_command("clear", "Clear the context being used by the Agent to start fresh")
def clear_context(client: Agent) -> str:
    client.clear_current_context()
    return "Context cleared"

@harness_command("models", "Get all Models available for use")
def get_models(client: Agent) -> str:
    return_message = f"Current model for agent is {bold(client._model)}.\n\nFull List of Models:"
    models = llmClientFactory.list_model_names()
    for model in models:
        return_message += f"\n- {model}"

    return return_message

