import sqlite3

# ---------------------------------------------------------
# INSERT USER
# ---------------------------------------------------------
def insert_user(conn, username, password_hash, role):
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, password_hash, role)
        )
        conn.commit()
        return True, "User created successfully."

    except sqlite3.IntegrityError:
        return False, "Username already exists."


# ---------------------------------------------------------
# GET USER BY USERNAME
# ---------------------------------------------------------
def get_user_by_username(conn, username):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    return cursor.fetchone()


# ---------------------------------------------------------
# VERIFY LOGIN
# ---------------------------------------------------------
def validate_login(conn, username):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, password_hash, role FROM users WHERE username = ?",
        (username,)
    )
    return cursor.fetchone()
