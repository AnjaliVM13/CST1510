"""
Chat History Persistence Module
Manages saving and loading of user chat histories to/from JSON files.
Provides persistent storage for AI conversation history across sessions.
"""

import os
import json
from pathlib import Path

# Data directory for storing chat history files
DATA_DIR = Path("DATA")


class ChatHistory:
    """
    Manages chat history persistence for users.
    Stores chat conversations in JSON format for retrieval across sessions.
    """

    def __init__(self, data_dir=DATA_DIR):
        """
        Initialize ChatHistory with data directory path.
        
        Args:
            data_dir: Directory path for storing chat history files
        """
        self.data_dir = Path(data_dir)
        # Create directory if it doesn't exist
        self.data_dir.mkdir(exist_ok=True)

    def get_chat_path(self, user_id):
        """
        Get the file path for a user's chat history JSON file.
        
        Args:
            user_id: Unique user identifier
            
        Returns:
            Path: Full path to user's chat history file
        """
        return self.data_dir / f"chat_{user_id}.json"

    def load_chat(self, user_id):
        """
        Load chat history for a specific user from JSON file.
        
        Args:
            user_id: Unique user identifier
            
        Returns:
            list: List of chat messages (empty list if file doesn't exist or error occurs)
        """
        path = self.get_chat_path(user_id)

        # Return empty list if file doesn't exist
        if not path.exists():
            return []

        try:
            # Read and parse JSON file
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            # Return empty list on any error (corrupted file, etc.)
            return []

    def save_chat(self, history, user_id):
        """
        Save chat history for a specific user to JSON file.
        
        Args:
            history: List of chat messages to save
            user_id: Unique user identifier
        """
        path = self.get_chat_path(user_id)

        # Write chat history to JSON file with pretty formatting
        with open(path, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4, ensure_ascii=False)

    def clear_chat(self, user_id):
        """
        Clear chat history for a specific user by deleting their JSON file.
        
        Args:
            user_id: Unique user identifier
        """
        path = self.get_chat_path(user_id)
        # Delete file if it exists
        if path.exists():
            path.unlink()


# Backward compatibility wrapper functions
def load_chat(user_id):
    """Load chat history for a specific user - backward compatibility."""
    chat_manager = ChatHistory()
    return chat_manager.load_chat(user_id)


def save_chat(history, user_id):
    """Save chat for a specific user - backward compatibility."""
    chat_manager = ChatHistory()
    return chat_manager.save_chat(history, user_id)
