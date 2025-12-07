from litellm import completion
from typing import List, Dict
import json

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

mystr = """
write me a function that splits lines of string and returns all lines that lie between two "```" blocks. for instance:
eqweqwewq
```action
hello world
```
dasddasdasdasdas
must return hello world"""
generate_response([{"role": "user", "content": mystr}])
#%%
def list_files():
    None

def read_file():
    None
    
def parse_action(response: str) -> Dict:
    """Parse the LLM response into a structured action dictionary."""
    try:
        response = extract_markdown_block(response, "action")
        response_json = json.loads(response)
        if "tool_name" in response_json and "args" in response_json:
            return response_json
        else:
            return {"tool_name": "error", "args": {"message": "You must respond with a JSON tool invocation."}}
    except json.JSONDecodeError:
        return {"tool_name": "error", "args": {"message": "Invalid JSON response. You must respond with a JSON tool invocation."}}
    
    
def extract_markdown_block(text): 
    """ 
    Extracts all lines that lie between ```` ``` ```` blocks from a string.
    
      Args:
         text (str): Input string containing markdown-style code blocks 
             Returns: 
        list: List of strings containing content between ```` ``` ```` blocks 
    """     
    if not '```' in response:
        return response
    lines = text.split('\\n') 
    result = [] 
    in_code_block = False     
    current_block = []          
    for line in lines: 
        if line.strip() == '```': 
            if in_code_block: 
                # End of code block - add content to result 
                result.append('\\n'.join(current_block))
                current_block = [] 
                in_code_block = False 
            else: 
                # Start of code block 
                in_code_block = True 
        elif in_code_block: 
            # We\'re inside a code block, collect the line 
            current_block.append(line) 
     
    return result 

#%%
agent_rules = [{
    "role": "system",
    "content": """ 
   You are an AI agent that can perform tasks by using available tools.

Available tools:
- list_files() -> List[str]: List all files in the current directory.
- read_file(file_name: str) -> str: Read the content of a file.
- terminate(message: str): End the agent loop and print a summary to the user.

If a user asks about files, list them before reading.

Every response MUST have an action, but can also include your reasoning.
Respond in this markdown format:

```action
{
    "tool_name": "insert tool_name",
    "args": {...fill in any required arguments here...}
}
```

Example question from user: 
"Hello i need to find a specific file about {topic}"

Your output must then be:
```action
{
    "tool_name": "list_files()",
    "args": ""
}
```

Afterwards, the output will be provided to you e.g.:
[recipes.txt, warcrimes.pdf, kittens.gif]

You can then guess which file would be most relevant and ask to read that file:
```action
{
    "tool_name": "read_file()",
    "args": "recipes.txt"
}
```
"""
}]


generate_response(agent_rules)
#%%
"""
function to list files and read their contents
"""
if __name__ == "__main__":
    iterations = 0
    max_iterations = 10
    memory = []
    # The Agent Loop
    while iterations < max_iterations:
    
        # 1. Construct prompt: Combine agent rules with memory
        prompt = agent_rules + memory
    
        # 2. Generate response from LLM
        print("Agent thinking...")
        response = generate_response(prompt)
        print(f"Agent response:\n {response}")
    
        # 3. Parse response to determine action
        action = parse_action(response)
    
        result = "Action executed"
    
        if action["tool_name"] == "list_files":
            result = {"result":list_files()}
        elif action["tool_name"] == "read_file":
            result = {"result":read_file(action["args"]["file_name"])}
        elif action["tool_name"] == "error":
            result = {"error":action["args"]["message"]}
        elif action["tool_name"] == "terminate":
            print(action["args"]["message"])
            break
        else:
            result = {"error":"Unknown action: "+action["tool_name"]}
    
        print(f"Action result: {result}")
    
        # 5. Update memory with response and results
        memory.extend([
            {"role": "assistant", "content": response},
            {"role": "user", "content": json.dumps(result)}
        ])
    
        # 6. Check termination condition
        if action["tool_name"] == "terminate":
            break
    
        iterations += 1