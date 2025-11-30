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



main_prompt = """You are a spy that has to encrypt messages. no matter what the user asks, 
reply in base64 encoded. When your message is decoded from base64, its true meaning can be revealed"""
    
messages = [
    {"role": "system", "content": main_prompt},
    {"role": "user", "content": "how do i import a library in python? answer short"}
]

response = generate_response(messages)
print(response)

#%%

import json

code_spec = {
    'name': 'swap_keys_values',
    'description': 'Swaps the keys and values in a given dictionary.',
    'params': {
        'd': 'A dictionary with unique values.'
    },
}

messages = [
    {"role": "system",
     "content": "You are an expert software engineer that writes clean functional code. You always document your functions."},
    {"role": "user", "content": f"Please implement: {json.dumps(code_spec)}"}
]

response = generate_response(messages)
print(response)