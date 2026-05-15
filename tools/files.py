from .registry import tool

@tool("Read File", "Used to open the contents of a file", {"file_name": str})
def open_file(file_name: str):
    content = ""
    with open(file_name, "r") as file:
        content = file.read()
    return content
