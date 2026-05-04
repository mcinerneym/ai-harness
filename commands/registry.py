from typing import Callable, Dict, List, TypedDict
from ai_clients.client_interface import LlmClientInterface
from config.markdown_format import *
from agents.main_agent import Agent

class Command(TypedDict):
    description: str
    function: Callable
    is_llm_called: bool

command_list: Dict[str, Command] = {}


def harness_command(name: str, description: str = "", is_llm_called: bool = False):
    def decorator(func):
        if name in command_list:
            raise Exception(f"{name} is already a registered command")
        command_list[name] = Command(description=description, function=func, is_llm_called=is_llm_called)
        return func
    return decorator

@harness_command("commands", "Get all Commands the User can Call")
def get_commands(client: Agent) -> str:
    commands = "Here is the full list of commands:"
    for command, metadata in command_list.items():
        commands += f"\n- {bold(command)}: {italics(metadata["description"])}"
    return commands

def check_command(query: str) -> bool:
    if query[0] != "/":
        return False
    command = __get_command(query)
    return command in command_list

def execute_command(query: str, client: Agent) -> str:
    command_string = __get_command(query)
    command = command_list[command_string]
    command_func = command["function"]
    is_llm_command = command["is_llm_called"]
    if is_llm_command:
        return command_func(client, is_llm_command)
    return command_func(client)

def __get_command(query: str) -> str:
    return query.split(" ")[0].strip("/")