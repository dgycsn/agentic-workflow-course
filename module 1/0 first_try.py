from litellm import completion


model = "qwen3-coder:30b"

response = completion(
    model="ollama/" + model,
    messages=[{"role": "user", "content": "hello"}]
)

message = response.choices[0].message.content
print(message)

#%%

from typing import List, Dict


def generate_response(messages: List[Dict]) -> str:
    """Call LLM to get response"""
    response = completion(
        model="ollama/" + model,
        messages=messages,
        max_tokens=1024
    )
    return response.choices[0].message.content


messages = [
    {"role": "system", "content": "You are an expert software engineer that prefers functional programming."},
    {"role": "user", "content": "Write a function to swap the keys and values in a dictionary."}
]

response = generate_response(messages)
print(response)