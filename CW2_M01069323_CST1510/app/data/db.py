import sqlite3
from pathlib import Path

DB_PATH = Path("DATA") / "intelligence_platform.db"

def connect_database(db_path=DB_PATH):
    """
    Connect to the SQLite database (Streamlit-safe).
    """

    db_path.parent.mkdir(exist_ok=True)

    conn = sqlite3.connect(
        str(db_path),
        check_same_thread=False,   #  allows Streamlit to use connection safely
        timeout=10                 #  prevents "database is locked"
    )

    conn.execute("PRAGMA foreign_keys = ON;")

    return conn
