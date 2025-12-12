import pandas as pd
from datetime import datetime


# ============================================================
# IT TICKET CLASS (OOP)
# ============================================================
class ITTicket:
    """ITTicket class for managing IT ticket data and operations."""

    def __init__(
        self,
        conn,
        ticket_id=None,
        priority=None,
        description=None,
        status=None,
        assigned_to=None,
        created_at=None,
        resolution_time_hours=None,
        inserted_at=None,
    ):
        """Initialize an ITTicket instance."""
        self.conn = conn
        self.ticket_id = ticket_id
        self.priority = priority
        self.description = description
        self.status = status
        self.assigned_to = assigned_to
        self.created_at = created_at
        self.resolution_time_hours = resolution_time_hours
        self.inserted_at = inserted_at

    @classmethod
    def from_db_row(cls, conn, db_row):
        """Create ITTicket instance from database row."""
        if db_row is None:
            return None
        return cls(
            conn=conn,
            ticket_id=db_row[0] if len(db_row) > 0 else None,
            priority=db_row[1] if len(db_row) > 1 else None,
            description=db_row[2] if len(db_row) > 2 else None,
            status=db_row[3] if len(db_row) > 3 else None,
            assigned_to=db_row[4] if len(db_row) > 4 else None,
            created_at=db_row[5] if len(db_row) > 5 else None,
            resolution_time_hours=db_row[6] if len(db_row) > 6 else None,
            inserted_at=db_row[7] if len(db_row) > 7 else None,
        )

    def save(self):
        """Save ticket to database."""
        if self.ticket_id is None:
            self.ticket_id = f"T{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}"

        query = """
            INSERT INTO it_tickets 
            (ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?)
        """

        self.conn.execute(
            query,
            (
                self.ticket_id,
                self.priority,
                self.description,
                self.status,
                self.assigned_to,
                self.resolution_time_hours,
            ),
        )
        self.conn.commit()

        return self.ticket_id

    def update_status(self, new_status):
        """Update ticket status."""
        query = """
            UPDATE it_tickets
            SET status = ?
            WHERE ticket_id = ?
        """
        self.conn.execute(query, (new_status, self.ticket_id))
        self.conn.commit()
        self.status = new_status

    def to_dict(self):
        """Convert ticket to dictionary."""
        return {
            "ticket_id": self.ticket_id,
            "priority": self.priority,
            "description": self.description,
            "status": self.status,
            "assigned_to": self.assigned_to,
            "created_at": self.created_at,
            "resolution_time_hours": self.resolution_time_hours,
            "inserted_at": self.inserted_at,
        }

    @classmethod
    def get_all(cls, conn):
        """Get all tickets as DataFrame."""
        query = """
            SELECT ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours
            FROM it_tickets
            ORDER BY created_at DESC
        """
        return pd.read_sql_query(query, conn)

    @classmethod
    def get_priority_counts(cls, conn):
        """Get ticket counts by priority."""
        query = """
            SELECT priority, COUNT(*) AS count
            FROM it_tickets
            GROUP BY priority
            ORDER BY count DESC
        """
        return pd.read_sql_query(query, conn)


# ============================================================
# BACKWARD COMPATIBILITY WRAPPER FUNCTIONS
# ============================================================
def insert_ticket(
    conn, priority, description, status, assigned_to, resolution_time_hours
):
    """Insert ticket - backward compatibility wrapper."""
    ticket = ITTicket(
        conn=conn,
        priority=priority,
        description=description,
        status=status,
        assigned_to=assigned_to,
        resolution_time_hours=resolution_time_hours,
    )
    return ticket.save()


def get_all_tickets(conn):
    """Get all tickets - backward compatibility wrapper."""
    return ITTicket.get_all(conn)


def update_ticket_status(conn, ticket_id, new_status):
    """Update ticket status - backward compatibility wrapper."""
    query = """
        UPDATE it_tickets
        SET status = ?
        WHERE ticket_id = ?
    """
    conn.execute(query, (new_status, ticket_id))
    conn.commit()


def get_ticket_priority_counts(conn):
    """Get ticket priority counts - backward compatibility wrapper."""
    return ITTicket.get_priority_counts(conn)
