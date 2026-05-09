from typing import List
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.text import Text
from rich.layout import Layout
from ai_clients.gemini import gemini_class
from ai_clients.client_interface import LlmClientInterface
from commands.registry import check_command, execute_command
from commands.system import *
from commands.llm import *
from config.rich_format import *
from agents.main_agent import Agent


def create_layout() -> Layout:
    layout = Layout()

    layout.split(
        Layout(name="main", ratio=4),
        Layout(name="status", size=3)
    )

    layout["main"].split_row(
        Layout(name="history", ratio=1),
        Layout(name="current", ratio=1)
    )

    return layout

def llm_loop():
    client: LlmClientInterface = gemini_class
    agent: Agent = Agent(client)
    console = Console()
    layout = create_layout()
    chat_history = []
    state = {
        "current_response": "",
        "status_text": "Ready"
    }

    console.print(Panel(Markdown("# Welcome to the Harness"), border_style=SYSTEM_CONSOLE_COLOR))

    # Create panels once — mutate .renderable in place, never recreate
    history_panel = Panel(
        Markdown("No Conversation History Yet"),
        title="Chat History",
        border_style="green"
    )
    current_panel = Panel(
        Text("Waiting for next response"),
        title="Agent",
        border_style=MODEL_CONSOLE_COLOR
    )
    status_panel = Panel(
        Text("Ready", style="bold cyan"),
        title="Status",
        border_style="blue"
    )

    # Assign panels to layout regions once
    layout["history"].update(history_panel)
    layout["current"].update(current_panel)
    layout["status"].update(status_panel)

    def update_display():
        """Mutate panel renderables in place — no layout reassignment needed."""
        history_content = "\n\n".join([
            f"**You:** {msg['query']}\n**Agent:** {msg['response']}"
            for msg in chat_history[-5:]
        ]) if chat_history else "No Conversation History Yet"

        history_panel.renderable = Markdown(history_content)
        current_panel.renderable = (
            Markdown(state["current_response"])
            if state["current_response"]
            else Text("Waiting for next response")
        )
        status_panel.renderable = Text(state["status_text"], style="bold cyan")
        # No layout[...].update() needed — panels are already referenced

    # auto_refresh=False: only re-render when YOU call live.refresh()
    with Live(layout, console=console, auto_refresh=False, screen=True) as live:
        while True:
            try:
                # Pause live, grab input, resume — no stop/start needed
                query = live.console.input("> ")

                if check_command(query.lower()):
                    command_response = execute_command(query.lower(), agent)
                    state["status_text"] = f"Executed command: {query.lower()}"
                    update_display()
                    live.refresh()
                else:
                    state["current_response"] = ""
                    state["status_text"] = "Generating response..."
                    update_display()
                    live.refresh()

                    full_response = ""
                    for chunk in agent.call_llm_stream(query):
                        full_response += chunk
                        state["current_response"] = full_response
                        update_display()
                        live.refresh()  # Only redraws when a chunk arrives

                    chat_history.append({"query": query, "response": full_response})
                    state["status_text"] = f"Response complete ({len(full_response)} chars)"
                    update_display()
                    live.refresh()

            except KeyboardInterrupt:
                break
            except Exception as e:
                state["status_text"] = f"Error: {str(e)}"
                update_display()
                live.refresh()