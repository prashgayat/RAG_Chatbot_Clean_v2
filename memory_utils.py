import json
import os
from collections import deque

# Ensure that the directory for storing memory exists
if not os.path.exists("chat_memory"):
    os.makedirs("chat_memory")

# Store memory for a session
def store_memory(session_id, query, answer):
    memory_file = f"chat_memory/{session_id}.json"
    
    # Retrieve existing memory or create a new one
    if os.path.exists(memory_file):
        with open(memory_file, "r") as file:
            memory_data = json.load(file)
    else:
        memory_data = {"questions": deque(maxlen=5), "answers": deque(maxlen=5)}
    
    memory_data["questions"].append(query)
    memory_data["answers"].append(answer)
    
    # Convert deque to list for JSON serialization
    memory_data["questions"] = list(memory_data["questions"])
    memory_data["answers"] = list(memory_data["answers"])
    
    # Save updated memory back to the file
    with open(memory_file, "w") as file:
        json.dump(memory_data, file)

# Retrieve memory for a session
def retrieve_memory(session_id):
    memory_file = f"chat_memory/{session_id}.json"
    
    if os.path.exists(memory_file):
        with open(memory_file, "r") as file:
            memory_data = json.load(file)
        return memory_data["questions"], memory_data["answers"]
    else:
        return [], []
    
# Reset memory for a session
def reset_chat_history(session_id):
    memory_file = f"chat_memory/{session_id}.json"
    if os.path.exists(memory_file):
        os.remove(memory_file)
