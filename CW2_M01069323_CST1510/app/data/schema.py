def create_users_table(conn):
    """
    Create the users table if it doesn't exist.
    
    This is a COMPLETE IMPLEMENTATION as an example.
    Study this carefully before implementing the other tables!
    
    Args:
        conn: Database connection object
    """
    cursor = conn.cursor()
    
    # SQL statement to create users table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    cursor.execute(create_table_sql)
    conn.commit()
    print(" Users table created successfully!")

def create_cyber_incidents_table(conn):
    """
    Create the cyber_incidents table.
    """
    cursor = conn.cursor()

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS cyber_incidents (
        incident_id TEXT UNIQUE,
        timestamp TEXT,
        severity TEXT,
        category TEXT,
        status TEXT,
        description TEXT,
        inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """

    cursor.execute(create_table_sql)
    conn.commit()
    print(" Cyber Incidents table created successfully!")


def create_datasets_metadata_table(conn):
    """
    Create the datasets_metadata table.
    """
    cursor = conn.cursor()

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

    cursor.execute(create_table_sql)
    conn.commit()
    print(" Datasets Metadata table created successfully!")



def create_it_tickets_table(conn):
    """
    Create the it_tickets table.
    """
    cursor = conn.cursor()

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

    cursor.execute(create_table_sql)
    conn.commit()
    print(" IT Tickets table created successfully!")


def create_all_tables(conn):
    """Create all tables."""
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_datasets_metadata_table(conn)
    create_it_tickets_table(conn)