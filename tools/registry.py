from typing import TypedDict, Callable, List

class HarnessTool(TypedDict):
    name: str
    description: str
    function: Callable

tool_registry: List[HarnessTool] = []

def tool(name: str, description: str):
    def decorator(func, *args, **kwargs):
        tool_registry.append(HarnessTool(name=name, description=description, function=func))
        return func(args, kwargs)
    return decorator