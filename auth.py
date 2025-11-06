import bcrypt
import os
USER_DATA_FILE = "users.txt"


def hash_password(plain_text_password):
    """Hashes a password using bcrypt."""
    # TODO: Encode the password to bytes (bcrypt requires byte strings) 
    password_bytes = plain_text_password.encode('utf-8')

    # TODO: Generate a salt using bcrypt.gensalt()
    salt = bcrypt.gensalt()

    # TODO: Hash the password using bcrypt.hashpw() 
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode('utf-8')

    """
    Verifies a plaintext password against a stored bcrypt
    hash.
    Args:
        plain_text_password (str): The password to verify
        hashed_password (str): The stored hash to check
        against
    Returns:
        bool: True if the password matches, False
        otherwise
    """
def verify_password(plain_text_password, hashed_password):
    # TODO: Encode both the plaintext password and the stored hash to bytes [cite: 43]
    password_bytes = plain_text_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')

    # TODO: Use bcrypt.checkpw() to verify the password
    # This function extracts the salt from the hash and compares
    return bcrypt.checkpw(password_bytes, hashed_bytes)


# TEMPORARY TEST CODE - Remove after testing
if __name__ == "__main__":
    test_password = "SecurePassword123"

    # Hash the password
    hashed = hash_password(test_password)
    print(f"Original Password: {test_password}")
    print(f"Hashed Password: {hashed}")
    print(f"Hash Length: {len(hashed)} characters")

    # Verify with correct password
    print(f"\nVerification with correct password: {verify_password(test_password, hashed)}")

    # Verify with incorrect password
    print(f"Verification with incorrect password: {verify_password('WrongPassword', hashed)}")

def register_user(username, password):
    """Registers a new user and saves to file if not already registered."""
    # Check if username already exists
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            for line in f:
                existing_username = line.strip().split(',')[0]
                if existing_username == username:
                    print(f"Error: Username '{username}' already exists.")
                    return False

    # Hash the password
    hashed_password = hash_password(password)

    # Append new user to file
    with open(USER_DATA_FILE, 'a') as f:
        f.write(f"{username},{hashed_password}\n")

    print(f"Success: User '{username}' registered successfully!")
    return True

    
    # TODO: Hash the password
    hashed_password = hash_password(password)

    # TODO: Append the new user to the file
    with open(USER_DATA_FILE, 'a') as f:
        f.write(f"{username},{hashed_password}\n")
    # Format: username,hashed_password
    print("User registered successfully.")
    return True

def user_exists(username):
 # TODO: Handle the case where the file doesn't exist yet
    if not os.path.exists(USER_DATA_FILE):
        return False
 # TODO: Read the file and check each line for the username
    with open(USER_DATA_FILE, 'r') as f:
        for line in f:
            existing_username = line.split(',')[0]
            if existing_username == username:
                return True
            
def login_user(username, password):
    """Logs in a user if credentials are correct."""
    # Handle case where user file does not exist
    if not os.path.exists(USER_DATA_FILE):
        print("Error: Username not found.")
        return False

    with open(USER_DATA_FILE, 'r') as f:
        for line in f:
            existing_username, stored_hashed_password = line.strip().split(',')
            if existing_username == username:
                # Verify password
                if verify_password(password, stored_hashed_password):
                    print(f"Success: Welcome, {username}!")
                    return True
                else:
                    print("Error: Invalid password.")
                    return False

    # Username not found
    print("Error: Username not found.")
    return False


def validate_username(username):
    """Validates the username according to basic rules."""
    if len(username) < 3:
        return False, "Username must be at least 3 characters long."
    if " " in username:
        return False, "Username cannot contain spaces."
    if not username.isalnum():
        return False, "Username must be alphanumeric (letters and numbers only)."
    return True, ""

1

def validate_password(password):
    """Validates the password according to security rules."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one number."
    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter."
    if not any(char.islower() for char in password):
        return False, "Password must contain at least one lowercase letter."
    if not any(char in "!@#$%^&*()-_=+[]{};:,<.>/?\\|`~" for char in password):
        return False, "Password must contain at least one special character."
    return True, ""


def display_menu():
    """Displays the main menu options."""
    print("\n" + "="*50)
    print("  MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print("  Secure Authentication System")
    print("="*50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)

def main():
    """Main program loop."""
    print("\nWelcome to the Week 7 Authentication System!")
    
    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()
        
        if choice == '1':
            # Registration flow
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()
            
            # Validate username
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue
            
            password = input("Enter a password: ").strip()

            
            # Validate password
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue
            
            # Confirm password
            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue
            
            # Register the user
            register_user(username, password)
        
        elif choice == '2':
            # Login flow
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            
            # Attempt login
            if login_user(username, password):
                print("\nYou are now logged in.")
                print("In a real application, you would now access the protected resources.")
                
                # Optional: Ask if they want to logout or exit
                input("\nPress Enter to return to main menu...")
        
        elif choice == '3':
            # Exit
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break
        
        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")
if __name__ == "__main__":
    main()



