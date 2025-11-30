"""
For practice, we are going to write a quasi-agent that can write Python functions based on user requirements. 
It isn’t quite a real agent, it can’t react and adapt, but it can do something useful for us.

The quasi-agent will ask the user what they want code for, write the code for the function, add documentation,
 and finally include test cases using the unittest framework. 
 This exercise will help you understand how to maintain context across multiple prompts 
 and manage the information flow between the user and the LLM. It will also help you understand the 
 pain of trying to parse and handle the output of an LLM that is not always consistent.
 
 
This exercise will allow you to practice programmatically sending prompts to an LLM and managing memory.

For this exercise, you should write a program that uses sequential prompts to generate any Python 
function based on user input. The program should:

First Prompt:

Ask the user what function they want to create
Ask the LLM to write a basic Python function based on the user’s description
Store the response for use in subsequent prompts
Parse the response to separate the code from the commentary by the LLM
Second Prompt:

Pass the code generated from the first prompt
Ask the LLM to add comprehensive documentation including:
Function description
Parameter descriptions
Return value description
Example usage
Edge cases
Third Prompt:

Pass the documented code generated from the second prompt
Ask the LLM to add test cases using Python’s unittest framework
Tests should cover:
Basic functionality
Edge cases
Error cases
Various input scenarios
Requirements:

Use the LiteLLM library
Maintain conversation context between prompts
Print each step of the development process
Save the final version to a Python file
If you want to practice further, try using the system message to force the LLM to always output 
code that has a specific style or uses particular libraries.
"""
#%%
from litellm import completion
from typing import List, Dict

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
first_prompt_1 = "You are an expert software engineer in python. Greet the user and ask how you can help them"
first_prompt_2 = "You are an expert software engineer in python. Based on the users request write a short function without documentation and print without any additional comments"


messages = []
messages.append({"role": "system", "content": first_prompt_1})
response = generate_response(messages)
print(response)

messages.append({"role": "assistant", "content": response})

user_reply = "hello! i want a function that creates an n by n random matrix"
messages.append({"role": "user", "content": user_reply})
messages.append({"role": "system", "content": first_prompt_2})
response = generate_response(messages)
print(response)

""" important note:
    ```python is the markdown syntax to highlight
"""
#%%
lines = response.strip().splitlines()
# Remove first and last line
parsed_code = "\n".join(lines[1:-1])

#%%
second_prompt_1 = """You are an expert software engineer in python.
you will now receive a python code written without documentation.
Do not change the code itself.
Add comments in code in order to give comprehensive documentation including:
Function description
Parameter descriptions
Return value description
Example usage
Edge cases."""
messages_prompt2 = []
messages_prompt2.append({"role": "system", "content": second_prompt_1})
messages_prompt2.append({"role": "user", "content": parsed_code})

response_2 = generate_response(messages_prompt2)
print(response_2)


#%%
lines = response_2.strip().splitlines()
# Remove first and last line
documented_code = "\n".join(lines[1:-1])
#%%

third_prompt_1 = """You are an expert software engineer in python.
you will now receive a python code written with documentation.
You now have to add test cases using Python’s unittest framework
Tests should cover:
Basic functionality
Edge cases
Error cases
Various input scenarios"""
messages_prompt3 = []
messages_prompt3.append({"role": "system", "content": third_prompt_1})
messages_prompt3.append({"role": "user", "content": documented_code})

response_3 = generate_response(messages_prompt3)
print(response_3)

#%%
"""
takeaways:
    you can also append messages to the same dict
    but parse inputs so llm is focused
    i hardcoded removing the md highlighting, but one could also 
    parse the output, and append only that to the messages
    
    also split task into multiple steps to make it manageable

"""
