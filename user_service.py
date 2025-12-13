import bcrypt
from pathlib import Path

from app.data.db import connect_database
from app.data.users import insert_user, get_user_by_username, User

DATA_DIR = Path("DATA")


class UserService:
    """Service class for user authentication and management operations."""

    def __init__(self, conn=None):
        """Initialize UserService with optional database connection."""
        self.conn = conn
        self.role_mapping = {
            "Cyber Security": "cyber",
            "Data Analyst": "data",
            "IT Support": "it",
        }

    def register_user(self, username, password, role="user"):
        """Register new user with password hashing."""
        if not self.conn:
            raise ValueError("Database connection required")

        # Normalize role
        role = self.role_mapping.get(role, role.lower())

        # Hash password
        password_hash = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        # Insert user into DB
        success, msg = insert_user(self.conn, username, password_hash, role)
        return success, msg

    def login_user(self, username, password):
        """Authenticate user and return their role."""
        if not self.conn:
            raise ValueError("Database connection required")

        user = get_user_by_username(self.conn, username)

        if not user:
            return False, "User not found."

        stored_hash = user[2]  # password_hash
        role = user[3]  # role column

        if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
            return True, role

        return False, "Incorrect password."

    def migrate_users_from_file(self):
        """Migrate users from users.txt file to database."""
        if not self.conn:
            raise ValueError("Database connection required")

        users_file = DATA_DIR / "users.txt"

        if not users_file.exists():
            print(f"Users file not found: {users_file}")
            return 0

        migrated_count = 0

        try:
            with open(users_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue

                    parts = line.split(",")
                    if len(parts) >= 3:
                        username = parts[0].strip()
                        password_hash = parts[1].strip()
                        role = parts[2].strip()

                        # Check if user already exists
                        existing_user = get_user_by_username(self.conn, username)
                        if existing_user is None:
                            # User doesn't exist, insert it
                            success, msg = insert_user(
                                self.conn, username, password_hash, role
                            )
                            if success:
                                migrated_count += 1
                            else:
                                print(f"Failed to migrate user {username}: {msg}")
                        else:
                            print(f"User {username} already exists, skipping...")

        except Exception as e:
            print(f"Error reading users file: {e}")

        return migrated_count


# Backward compatibility wrapper functions
def register_user(conn, username, password, role="user"):
    """Register new user with password hashing - backward compatibility."""
    service = UserService(conn)
    return service.register_user(username, password, role)


def login_user(conn, username, password):
    """Authenticate user and return their role - backward compatibility."""
    service = UserService(conn)
    return service.login_user(username, password)


def migrate_users_from_file(conn):
    """Migrate users from users.txt file to database - backward compatibility."""
    service = UserService(conn)
    return service.migrate_users_from_file()
