import sqlite3
from pathlib import Path
from contextlib import contextmanager


# ALWAYS use absolute path to avoid Streamlit creating wrong DB copies
DB_PATH = Path(__file__).resolve().parents[2] / "DATA" / "intelligence_platform.db"


class DatabaseConnection:
    """Database connection manager with context manager support."""

    def __init__(self, db_path=DB_PATH):
        """Initialize database connection manager."""
        self.db_path = db_path
        self.conn = None

    def connect(self):
        """Connect to the SQLite database (Streamlit-safe)."""
        self.db_path.parent.mkdir(exist_ok=True)

        self.conn = sqlite3.connect(
            str(self.db_path),
            check_same_thread=False,  # allows Streamlit to use connection safely
            timeout=10,  # prevents "database is locked"
        )

        self.conn.execute("PRAGMA foreign_keys = ON;")
        return self.conn

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None

    def __enter__(self):
        """Context manager entry."""
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
        return False

    def __del__(self):
        """Cleanup on deletion."""
        self.close()


# Backward compatibility function
def connect_database(db_path=DB_PATH):
    """
    Connect to the SQLite database (Streamlit-safe).
    Backward compatibility wrapper.
    """
    db_path.parent.mkdir(exist_ok=True)

    conn = sqlite3.connect(
        str(db_path),
        check_same_thread=False,  # allows Streamlit to use connection safely
        timeout=10,  # prevents "database is locked"
    )

    conn.execute("PRAGMA foreign_keys = ON;")
    return conn
