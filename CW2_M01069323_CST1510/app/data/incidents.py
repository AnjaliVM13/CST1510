import pandas as pd

def insert_incident(conn, category, severity, status, description, reported_by=None):
    cursor = conn.cursor()

    query = """
    INSERT INTO cyber_incidents
    (category, severity, status, description, timestamp)
    VALUES (?, ?, ?, ?, datetime('now'))
    """

    cursor.execute(query, (category, severity, status, description))
    conn.commit()

    return cursor.lastrowid


def get_all_incidents(conn):
    query = "SELECT * FROM cyber_incidents"
    return pd.read_sql_query(query, conn)


def get_incidents_by_type_count(conn):
    """
    Count incidents by category (NOT incident_type).
    """
    query = """
    SELECT category, COUNT(*) AS count
    FROM cyber_incidents
    GROUP BY category
    ORDER BY count DESC
    """
    return pd.read_sql_query(query, conn)


def get_high_severity_by_status(conn):
    """
    High severity = severity='High'
    """
    query = """
    SELECT status, COUNT(*) AS count
    FROM cyber_incidents
    WHERE severity = 'High'
    GROUP BY status
    ORDER BY count DESC
    """
    return pd.read_sql_query(query, conn)


def get_incident_types_with_many_cases(conn, min_count=5):
    query = """
    SELECT category AS category, COUNT(*) AS count
    FROM cyber_incidents
    GROUP BY category
    HAVING COUNT(*) > ?
    ORDER BY count DESC
    """
    return pd.read_sql_query(query, conn, params=(min_count,))
