import bcrypt
from pathlib import Path

from app.data.db import connect_database
from app.data.users import insert_user, get_user_by_username

DATA_DIR = Path("DATA")

# ---------------------------------------------------------
# REGISTER USER
# ---------------------------------------------------------
def register_user(conn, username, password, role='user'):
    """Register new user with password hashing."""
    
    # Hash password
    password_hash = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    # Insert user into DB
    success, msg = insert_user(conn, username, password_hash, role)
    return success, msg


# ---------------------------------------------------------
# LOGIN USER
# ---------------------------------------------------------
def login_user(conn, username, password):
    """Authenticate user and return their role."""

    user = get_user_by_username(conn, username)

    if not user:
        return False, "User not found."

    stored_hash = user[2]   # password_hash
    role = user[3]          # role column

    if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
        return True, role

    return False, "Incorrect password."

