from typing import Callable, Dict, Any, List
"""
A - Actions

Actions define what the agent can do. 
Think of them as the agent’s toolkit. 
Each action is a discrete capability that can be executed in the environment. 
The action system has two main parts: the Action class and the ActionRegistry.

wrapper class:
    does not introduce anything new itself, 
    just wraps existing function(s) to add structure,metadata, control
    
**args: all keyword arguments into a dictionary
execute(name="Alice", age=30):
    args == {
        "name": "Alice",
        "age": 30
    }
def f(x, y): ...
f(1, 2)     --> positional
f(x=1, y=2) --> keyword

*-> tuple --> unpack positional arguments
**-> dictionary --> unpack keyword arguments
"""
import os

class Action:
    def __init__(self,
                 name: str,
                 function: Callable,
                 description: str,
                 parameters: Dict,
                 terminal: bool = False):
        self.name = name
        self.function = function
        self.description = description
        self.terminal = terminal
        self.parameters = parameters

    def execute(self, **args) -> Any:
        """Execute the action's function"""
        return self.function(**args)

class ActionRegistry:
    def __init__(self):
        self.actions = {}

    def register(self, action: Action):
        self.actions[action.name] = action

    def get_action(self, name: str) -> [Action, None]:
        """get action by its name, get its properties via .__dict__"""
        return self.actions.get(name, None)

    def get_actions(self) -> List[Action]:
        """Get all registered actions, read their names via .keys()"""
        return list(self.actions.values())
    
#%%

def list_files() -> list:
    """List all files in the current directory."""
    return os.listdir('.')

def read_file(file_name: str) -> str:
    """Read and return the contents of a file."""
    with open(file_name, 'r') as f:
        return f.read()

def search_in_file(file_name: str, search_term: str) -> list:
    """Search for a term in a file and return matching lines."""
    results = []
    with open(file_name, 'r') as f:
        for i, line in enumerate(f.readlines()):
            if search_term in line:
                results.append((i+1, line.strip()))
    return results

#%%

if __name__ == "__main__": 
    
    # Create and populate the action registry
    registry = ActionRegistry()
    
    registry.register(Action(
        name="list_files",
        function=list_files,
        description="List all files in the current directory",
        parameters={
            "type": "object",
            "properties": {},
            "required": []
        },
        terminal=False
    ))
    
    registry.register(Action(
        name="read_file",
        function=read_file,
        description="Read the contents of a specific file",
        parameters={
            "type": "object",
            "properties": {
                "file_name": {
                    "type": "string",
                    "description": "Name of the file to read"
                }
            },
            "required": ["file_name"]
        },
        terminal=False
    ))
    
    registry.register(Action(
        name="search_in_file",
        function=search_in_file,
        description="Search for a term in a specific file",
        parameters={
            "type": "object",
            "properties": {
                "file_name": {
                    "type": "string", 
                    "description": "Name of the file to search in"
                },
                "search_term": {
                    "type": "string",
                    "description": "Term to search for"
                }
            },
            "required": ["file_name", "search_term"]
        },
        terminal=False
    ))
