"""
Database Connection Module
Manages SQLite database connections with Streamlit-safe configuration.
Provides context manager support for proper connection handling.
"""

import sqlite3
from pathlib import Path
from contextlib import contextmanager


# ALWAYS use absolute path to avoid Streamlit creating wrong DB copies
# Construct absolute path to database file (2 levels up from this file, then DATA folder)
DB_PATH = Path(__file__).resolve().parents[2] / "DATA" / "intelligence_platform.db"


class DatabaseConnection:
    """Database connection manager with context manager support."""

    def __init__(self, db_path=DB_PATH):
        """Initialize database connection manager."""
        self.db_path = db_path
        self.conn = None

    def connect(self):
        """
        Connect to the SQLite database with Streamlit-safe configuration.
        Creates parent directory if needed and enables foreign key constraints.
        
        Returns:
            sqlite3.Connection: Database connection object
        """
        # Ensure parent directory exists before connecting
        self.db_path.parent.mkdir(exist_ok=True)

        # Create connection with Streamlit-compatible settings
        self.conn = sqlite3.connect(
            str(self.db_path),
            check_same_thread=False,  # allows Streamlit to use connection safely across threads
            timeout=10,  # prevents "database is locked" errors
        )

        # Enable foreign key constraints for referential integrity
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
    Backward compatibility wrapper for direct function calls.
    
    Args:
        db_path: Path to database file (defaults to DB_PATH)
        
    Returns:
        sqlite3.Connection: Database connection object
    """
    # Ensure parent directory exists
    db_path.parent.mkdir(exist_ok=True)

    # Create connection with Streamlit-compatible settings
    conn = sqlite3.connect(
        str(db_path),
        check_same_thread=False,  # allows Streamlit to use connection safely across threads
        timeout=10,  # prevents "database is locked" errors
    )

    # Enable foreign key constraints for referential integrity
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn
