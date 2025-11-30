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
    {"role": "user", "content": "How many eggs do i need for a cake? answer short plz"}
]

response = generate_response(messages)
print(response)

