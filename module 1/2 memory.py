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


messages = [
    {"role": "system", "content": "You are an expert software engineer that prefers functional programming but does not write documentation."},
    {"role": "user", "content": "Write a function to swap the keys and values in a dictionary."}
]

response = generate_response(messages)
print(response)

# Second query without including the previous response
badmessages = [
    {"role": "user", "content": "Update the function to include documentation."}
]

badresponse = generate_response(badmessages)
print(badresponse)

#%%

# Here is the assistant's response from the previous step
# with the code. This gives it "memory" of the previous
# interaction.
messages.append({"role": "assistant", "content": response},)
   
# Now, we can ask the assistant to update the function
messages.append({"role": "user", "content": "Update the function to include documentation."})


response = generate_response(messages)
print(response)