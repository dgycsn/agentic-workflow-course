"""
G - Goals / Instructions: 
    What the agent is trying to accomplish and 
    its instructions on how to try to achieve its goals.
"""

class Goal:
    def __init__(self, 
                 priority: int,
                 name: str,
                 description: str):
        self.priority = priority
        self.name = name
        self.description = description
        
        
if __name__ == "__main__":
    # Define a simple file management goal
    file_management_goal = Goal(
        priority=1,
        name="file_management",
        description="""Manage files in the current directory by:
        1. Listing files when needed
        2. Reading file contents when needed
        3. Searching within files when information is required
        4. Providing helpful explanations about file contents"""
    )