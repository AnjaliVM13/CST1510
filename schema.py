class DatabaseSchema:
    """Manages database schema creation and management."""

    def __init__(self, conn):
        """Initialize DatabaseSchema with database connection."""
        self.conn = conn
        self.cursor = conn.cursor()

    def create_users_table(self):
        """Create the users table if it doesn't exist."""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """

        self.cursor.execute(create_table_sql)
        self.conn.commit()
        print(" Users table created successfully!")

    def create_cyber_incidents_table(self):
        """Create the cyber_incidents table."""
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
        """Create all tables."""
        self.create_users_table()
        self.create_cyber_incidents_table()
        self.create_datasets_metadata_table()
        self.create_it_tickets_table()


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
