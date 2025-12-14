"""
User Service Module
Handles user authentication, registration, and migration from file-based storage.
Provides high-level user management operations with password hashing.
"""

import bcrypt
from pathlib import Path

# Database connection and user data access
from app.data.db import connect_database
from app.data.users import insert_user, get_user_by_username, User

# Data directory path for user migration files
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
        """
        Register new user with secure password hashing.
        
        Args:
            username: Desired username (must be unique)
            password: Plain text password (will be hashed)
            role: User role (default: "user")
            
        Returns:
            tuple: (success: bool, message: str) - Registration result
        """
        # Validate database connection exists
        if not self.conn:
            raise ValueError("Database connection required")

        # Normalize role name using mapping or lowercase conversion
        role = self.role_mapping.get(role, role.lower())

        # Hash password using bcrypt with auto-generated salt
        password_hash = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        # Insert user into database with hashed password
        success, msg = insert_user(self.conn, username, password_hash, role)
        return success, msg

    def login_user(self, username, password):
        """
        Authenticate user credentials and return their role if successful.
        
        Args:
            username: Username to authenticate
            password: Plain text password to verify
            
        Returns:
            tuple: (success: bool, role_or_message: str) - Authentication result
        """
        # Validate database connection exists
        if not self.conn:
            raise ValueError("Database connection required")

        # Retrieve user record from database
        user = get_user_by_username(self.conn, username)

        # Check if user exists
        if not user:
            return False, "User not found."

        # Extract stored password hash and role from user tuple
        stored_hash = user[2]  # password_hash column index
        role = user[3]  # role column index

        # Verify password against stored hash using bcrypt
        if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
            return True, role

        # Password verification failed
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
