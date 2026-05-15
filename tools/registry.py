from typing import TypedDict, Callable, List, Dict

class HarnessTool(TypedDict):
    name: str
    description: str
    parameters: Dict
    function: Callable

tool_registry: List[HarnessTool] = []

def tool(name: str, description: str, parameters: Dict):
    def decorator(func, *args, **kwargs):
        tool_registry.append(HarnessTool(name=name, description=description, parameters=parameters, function=func))
        return func(args, kwargs)
    return decorator