import pandas as pd
from datetime import datetime


# ============================================================
# SECURITY INCIDENT CLASS (OOP)
# ============================================================
class SecurityIncident:
    """SecurityIncident class for managing security incident data and operations."""

    def __init__(
        self,
        conn,
        incident_id=None,
        timestamp=None,
        severity=None,
        category=None,
        status=None,
        description=None,
        inserted_at=None,
    ):
        """Initialize a SecurityIncident instance."""
        self.conn = conn
        self.incident_id = incident_id
        self.timestamp = timestamp
        self.severity = severity
        self.category = category
        self.status = status
        self.description = description
        self.inserted_at = inserted_at

    @classmethod
    def from_db_row(cls, conn, db_row):
        """Create SecurityIncident instance from database row."""
        if db_row is None:
            return None
        return cls(
            conn=conn,
            incident_id=db_row[0] if len(db_row) > 0 else None,
            timestamp=db_row[1] if len(db_row) > 1 else None,
            severity=db_row[2] if len(db_row) > 2 else None,
            category=db_row[3] if len(db_row) > 3 else None,
            status=db_row[4] if len(db_row) > 4 else None,
            description=db_row[5] if len(db_row) > 5 else None,
            inserted_at=db_row[6] if len(db_row) > 6 else None,
        )

    def save(self):
        """Save incident to database."""
        cursor = self.conn.cursor()

        # Generate incident_id if not provided
        if self.incident_id is None:
            self.incident_id = f"INC{pd.Timestamp.now().strftime('%Y%m%d%H%M%S%f')}"

        query = """
        INSERT INTO cyber_incidents
        (incident_id, category, severity, status, description, timestamp)
        VALUES (?, ?, ?, ?, ?, datetime('now'))
        """
        cursor.execute(
            query,
            (
                self.incident_id,
                self.category,
                self.severity,
                self.status,
                self.description,
            ),
        )
        self.conn.commit()
        return self.incident_id

    def update_status(self, new_status):
        """Update incident status."""
        cursor = self.conn.cursor()
        query = """
        UPDATE cyber_incidents
        SET status = ?
        WHERE incident_id = ?
        """
        cursor.execute(query, (new_status, self.incident_id))
        self.conn.commit()
        self.status = new_status

    def delete(self):
        """Delete incident from database."""
        cursor = self.conn.cursor()
        query = "DELETE FROM cyber_incidents WHERE incident_id = ?"
        cursor.execute(query, (self.incident_id,))
        self.conn.commit()

    def to_dict(self):
        """Convert incident to dictionary."""
        return {
            "incident_id": self.incident_id,
            "timestamp": self.timestamp,
            "severity": self.severity,
            "category": self.category,
            "status": self.status,
            "description": self.description,
            "inserted_at": self.inserted_at,
        }

    @classmethod
    def get_all(cls, conn):
        """Get all incidents as DataFrame."""
        query = "SELECT * FROM cyber_incidents"
        return pd.read_sql_query(query, conn)

    @classmethod
    def get_by_type_count(cls, conn):
        """Count incidents by category."""
        query = """
        SELECT category, COUNT(*) AS count
        FROM cyber_incidents
        GROUP BY category
        ORDER BY count DESC
        """
        return pd.read_sql_query(query, conn)

    @classmethod
    def get_high_severity_by_status(cls, conn):
        """Get high severity incidents grouped by status."""
        query = """
        SELECT status, COUNT(*) AS count
        FROM cyber_incidents
        WHERE severity = 'High'
        GROUP BY status
        ORDER BY count DESC
        """
        return pd.read_sql_query(query, conn)

    @classmethod
    def get_types_with_many_cases(cls, conn, min_count=5):
        """Get incident types with many cases."""
        query = """
        SELECT category AS category, COUNT(*) AS count
        FROM cyber_incidents
        GROUP BY category
        HAVING COUNT(*) > ?
        ORDER BY count DESC
        """
        return pd.read_sql_query(query, conn, params=(min_count,))


# ============================================================
# BACKWARD COMPATIBILITY WRAPPER FUNCTIONS
# ============================================================
def insert_incident(conn, category, severity, status, description, reported_by=None):
    """Insert incident - backward compatibility wrapper."""
    incident = SecurityIncident(
        conn=conn,
        category=category,
        severity=severity,
        status=status,
        description=description,
    )
    return incident.save()


def get_all_incidents(conn):
    """Get all incidents - backward compatibility wrapper."""
    return SecurityIncident.get_all(conn)


def get_incidents_by_type_count(conn):
    """Get incidents by type count - backward compatibility wrapper."""
    return SecurityIncident.get_by_type_count(conn)


def get_high_severity_by_status(conn):
    """Get high severity by status - backward compatibility wrapper."""
    return SecurityIncident.get_high_severity_by_status(conn)


def get_incident_types_with_many_cases(conn, min_count=5):
    """Get incident types with many cases - backward compatibility wrapper."""
    return SecurityIncident.get_types_with_many_cases(conn, min_count)


def update_incident_status(conn, incident_id, new_status):
    """Update incident status - backward compatibility wrapper."""
    cursor = conn.cursor()
    # Try incident_id first, then fall back to rowid if it's numeric
    if isinstance(incident_id, (int, float)) or (
        isinstance(incident_id, str) and incident_id.isdigit()
    ):
        # Use rowid for backward compatibility with old code that used lastrowid
        query = """
        UPDATE cyber_incidents
        SET status = ?
        WHERE rowid = ?
        """
    else:
        query = """
        UPDATE cyber_incidents
        SET status = ?
        WHERE incident_id = ?
        """
    cursor.execute(query, (new_status, incident_id))
    conn.commit()


def delete_incident(conn, incident_id):
    """Delete incident - backward compatibility wrapper."""
    cursor = conn.cursor()
    # Try incident_id first, then fall back to rowid if it's numeric
    if isinstance(incident_id, (int, float)) or (
        isinstance(incident_id, str) and incident_id.isdigit()
    ):
        # Use rowid for backward compatibility with old code that used lastrowid
        query = "DELETE FROM cyber_incidents WHERE rowid = ?"
    else:
        query = "DELETE FROM cyber_incidents WHERE incident_id = ?"
    cursor.execute(query, (incident_id,))
    conn.commit()
