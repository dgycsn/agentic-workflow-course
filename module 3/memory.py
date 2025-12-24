from typing import Dict, List
"""
m- memory
 allow the agent to store and retrieve information about its interactions, 
 which is critical for context and decision-making. 
 
allow adding additional functionality later without changing the core loop
"""

class Memory:
    def __init__(self):
        self.items = []  # Basic conversation history

    def add_memory(self, memory: Dict):
        """Add memory to working memory"""
        self.items.append(memory)

    def get_memories(self, limit: int = None) -> List[Dict]:
        """Get formatted conversation history for prompt"""
        return self.items[:limit]