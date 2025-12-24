from goal import Goal
from action import Action, ActionRegistry
import functions
from agent import Agent
from environment import Environment
from schema import schema_from_function

from litellm import completion
from language import AgentFunctionCallingActionLanguage, Prompt
import json

#%%
model = "ollama/qwen3-coder:30b"

def generate_response(prompt: Prompt) -> str:
    """Call LLM to get response"""

    messages = prompt.messages
    tools = prompt.tools
    # print(tools)

    result = None

    if not tools:
        response = completion(
            model=model,
            messages=messages,
            max_tokens=1024
        )
        result = response.choices[0].message.content
    else:
        response = completion(
            model=model,
            messages=messages,
            tools=tools,
            max_tokens=1024
        )

        if response.choices[0].message.tool_calls:
            tool = response.choices[0].message.tool_calls[0]
            result = {
                "tool": tool.function.name,
                "args": json.loads(tool.function.arguments),
            }
            result = json.dumps(result)
        else:
            result = response.choices[0].message.content


    return result
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
        terminal=key[:6] == "termin"
    )
    action_registry.register(curraction)
    
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
final_memory = file_explorer_agent.run(user_input, max_iterations=20)

# Print the final conversation if desired
for item in final_memory.get_memories():
    print(f"\n{item['type'].upper()}: {item['content']}")