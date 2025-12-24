from goal import Goal
from action import Action, ActionRegistry
import functions
from agent import Agent, AgentLanguage
from environment import Environment
from schema import schema_from_function

from litellm import completion
from typing import List, Dict

#%%
model = "qwen3-coder:30b"

def generate_response(messages: List[Dict]) -> str:
    """Call LLM to get response"""
    response = completion(
        model="ollama/" + model,
        messages=messages,
        max_tokens=1024
    )
    return response.choices[0].message.content
#%%
goals = [
    Goal(
        priority=1, 
        name="Explore Files", 
        description="Explore files in the current directory by listing and reading them"
    ),
    Goal(
        priority=2, 
        name="Terminate", 
        description="Terminate the session when tasks are complete with a helpful summary"
    )
]

action_registry = ActionRegistry()

defined_funcs = {
    name: obj
    for name, obj in functions.__dict__.items()
    if callable(obj) and  obj.__module__ == "functions"
}

for key in defined_funcs.keys():
    curr_func = defined_funcs[key]
    parameted_scheme = schema_from_function(curr_func)
    curraction = Action(
        name=key,
        function=curr_func,
        description=curr_func.__doc__,
        parameters=parameted_scheme,
        terminal=True
    )
    
#%%
# Define the agent language and environment
agent_language = AgentFunctionCallingActionLanguage()
environment = Environment()
    
# Create the agent
file_explorer_agent = Agent(
    goals=goals,
    agent_language=agent_language,
    action_registry=action_registry,
    generate_response=generate_response,
    environment=environment
)

# Run the agent
user_input = input("What would you like me to do? ")
final_memory = file_explorer_agent.run(user_input, max_iterations=10)

# Print the final conversation if desired
for item in final_memory.get_memories():
    print(f"\n{item['type'].upper()}: {item['content']}")