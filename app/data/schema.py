"""
Database Schema Management Module
Handles creation and management of all database tables.
"""

class DatabaseSchema:
    """
    Manages database schema creation and management.
    Provides methods to create all required tables for the application.
    """

    def __init__(self, conn):
        """
        Initialize DatabaseSchema with database connection.
        
        Args:
            conn: SQLite database connection object
        """
        self.conn = conn
        # Get cursor for executing SQL commands
        self.cursor = conn.cursor()

    def create_users_table(self):
        """
        Create the users table if it doesn't exist.
        Stores user authentication credentials and role information.
        """
        # SQL statement to create users table with authentication fields
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  # Auto-incrementing primary key
            username TEXT NOT NULL UNIQUE,  # Unique username constraint
            password_hash TEXT NOT NULL,  # Bcrypt hashed password
            role TEXT DEFAULT 'user',  # User role (cyber, data, it, admin)
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  # Account creation timestamp
        )
        """

        # Execute SQL and commit transaction
        self.cursor.execute(create_table_sql)
        self.conn.commit()
        print(" Users table created successfully!")

    def create_cyber_incidents_table(self):
        """
        Create the cyber_incidents table if it doesn't exist.
        Stores cybersecurity incident records with severity, category, and status.
        """
        # SQL statement to create cyber incidents table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS cyber_incidents (
            incident_id TEXT UNIQUE,  # Unique incident identifier
            timestamp TEXT,  # When the incident occurred
            severity TEXT,  # Severity level (Critical, High, Medium, Low)
            category TEXT,  # Incident category/type
            status TEXT,  # Current status (Open, In Progress, Resolved, Closed)
            description TEXT,  # Detailed incident description
            inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  # Record insertion timestamp
        )
        """

        # Execute SQL and commit transaction
        self.cursor.execute(create_table_sql)
        self.conn.commit()
        print(" Cyber Incidents table created successfully!")

    def create_datasets_metadata_table(self):
        """Create the datasets_metadata table."""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS datasets_metadata (
            dataset_id TEXT UNIQUE,
            name TEXT NOT NULL,
            rows INTEGER,
            columns INTEGER,
            uploaded_by TEXT,
            upload_date TEXT
        )
        """

        self.cursor.execute(create_table_sql)
        self.conn.commit()
        print(" Datasets Metadata table created successfully!")

    def create_it_tickets_table(self):
        """Create the it_tickets table."""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS it_tickets (
            ticket_id TEXT UNIQUE NOT NULL,
            priority TEXT,
            description TEXT,
            status TEXT,
            assigned_to TEXT,
            created_at TEXT,
            resolution_time_hours REAL,
            inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """

        self.cursor.execute(create_table_sql)
        self.conn.commit()
        print(" IT Tickets table created successfully!")

    def create_all_tables(self):
        """
        Create all database tables in the correct order.
        Ensures all required tables exist before data operations.
        """
        # Create tables in dependency order
        self.create_users_table()  # Users table (no dependencies)
        self.create_cyber_incidents_table()  # Incidents table (no dependencies)
        self.create_datasets_metadata_table()  # Datasets table (no dependencies)
        self.create_it_tickets_table()  # IT tickets table (no dependencies)


# Backward compatibility wrapper functions
def create_users_table(conn):
    """Create the users table - backward compatibility."""
    schema = DatabaseSchema(conn)
    return schema.create_users_table()


def create_cyber_incidents_table(conn):
    """Create the cyber_incidents table - backward compatibility."""
    schema = DatabaseSchema(conn)
    return schema.create_cyber_incidents_table()


def create_datasets_metadata_table(conn):
    """Create the datasets_metadata table - backward compatibility."""
    schema = DatabaseSchema(conn)
    return schema.create_datasets_metadata_table()


def create_it_tickets_table(conn):
    """Create the it_tickets table - backward compatibility."""
    schema = DatabaseSchema(conn)
    return schema.create_it_tickets_table()


def create_all_tables(conn):
    """Create all tables - backward compatibility."""
    schema = DatabaseSchema(conn)
    return schema.create_all_tables()
