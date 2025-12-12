import sqlite3


# ============================================================
# USER CLASS (OOP)
# ============================================================
class User:
    """User class for managing user data and operations."""

    def __init__(
        self,
        conn,
        user_id=None,
        username=None,
        password_hash=None,
        role=None,
        created_at=None,
    ):
        """Initialize a User instance."""
        self.conn = conn
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.role = role
        self.created_at = created_at

    @classmethod
    def from_db_row(cls, conn, db_row):
        """Create User instance from database row."""
        if db_row is None:
            return None
        return cls(
            conn=conn,
            user_id=db_row[0],
            username=db_row[1],
            password_hash=db_row[2],
            role=db_row[3],
            created_at=db_row[4] if len(db_row) > 4 else None,
        )

    def save(self):
        """Save user to database."""
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (self.username, self.password_hash, self.role),
            )
            self.conn.commit()
            self.user_id = cursor.lastrowid
            return True, "User created successfully."
        except sqlite3.IntegrityError:
            return False, "Username already exists."

    @classmethod
    def get_by_username(cls, conn, username):
        """Get user by username."""
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        return cls.from_db_row(conn, row)

    def to_dict(self):
        """Convert user to dictionary."""
        return {
            "id": self.user_id,
            "username": self.username,
            "role": self.role,
            "created_at": self.created_at,
        }


# ============================================================
# BACKWARD COMPATIBILITY WRAPPER FUNCTIONS
# ============================================================
def insert_user(conn, username, password_hash, role):
    """Insert user - backward compatibility wrapper."""
    user = User(conn=conn, username=username, password_hash=password_hash, role=role)
    return user.save()


def get_user_by_username(conn, username):
    """Get user by username - backward compatibility wrapper."""
    user = User.get_by_username(conn, username)
    if user is None:
        return None
    # Return tuple format for backward compatibility
    return (user.user_id, user.username, user.password_hash, user.role, user.created_at)


def validate_login(conn, username):
    """Validate login - backward compatibility wrapper."""
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, password_hash, role FROM users WHERE username = ?",
        (username,),
    )
    return cursor.fetchone()
