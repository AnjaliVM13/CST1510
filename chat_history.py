import os
import json
from pathlib import Path

DATA_DIR = Path("DATA")


class ChatHistory:
    """Manages chat history persistence for users."""

    def __init__(self, data_dir=DATA_DIR):
        """Initialize ChatHistory with data directory."""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

    def get_chat_path(self, user_id):
        """Get the file path for a user's chat history."""
        return self.data_dir / f"chat_{user_id}.json"

    def load_chat(self, user_id):
        """Load chat history for a specific user."""
        path = self.get_chat_path(user_id)

        if not path.exists():
            return []

        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def save_chat(self, history, user_id):
        """Save chat for a specific user."""
        path = self.get_chat_path(user_id)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4, ensure_ascii=False)

    def clear_chat(self, user_id):
        """Clear chat history for a specific user."""
        path = self.get_chat_path(user_id)
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
