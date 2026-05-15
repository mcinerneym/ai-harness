from .registry import tool

@tool(name="Read File", description="Used to open the contents of a file")
def open_file(file_name: str):
    content = ""
    with open(file_name, "r") as file:
        content = file.read()
    return content
