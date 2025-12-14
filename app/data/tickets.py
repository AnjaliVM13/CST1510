"""
IT Ticket Data Management Module
Provides OOP interface for IT support ticket operations including creation, updates, and analytics.
"""

import pandas as pd
from datetime import datetime


# ============================================================
# IT TICKET CLASS (OOP)
# ============================================================
class ITTicket:
    """
    ITTicket class for managing IT ticket data and operations.
    Encapsulates ticket information and provides methods for database persistence and queries.
    """

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
        """
        Initialize an ITTicket instance with database connection and ticket attributes.
        
        Args:
            conn: Database connection object
            ticket_id: Unique ticket identifier (auto-generated if None)
            priority: Ticket priority level (High, Medium, Low)
            description: Ticket description/details
            status: Current status (Open, In Progress, Resolved, Closed)
            assigned_to: User assigned to handle the ticket
            created_at: Ticket creation timestamp
            resolution_time_hours: Time taken to resolve (in hours)
            inserted_at: Record insertion timestamp
        """
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
        """
        Save ticket to database. Creates new ticket record with auto-generated ID if needed.
        Handles various ticket_id formats and validates input.
        
        Returns:
            str: Ticket ID (generated or provided)
        """
        # Debug: Log what we received (only in Streamlit context)
        import streamlit as st

        if hasattr(st, "write"):
            st.write(
                f"🔍 ITTicket.save() - Received ticket_id: {repr(self.ticket_id)} (type: {type(self.ticket_id).__name__})"
            )

        # Only generate ticket_id if it's None, empty string, or just whitespace
        # Convert to string first to handle any numeric types
        original_ticket_id = self.ticket_id
        if self.ticket_id is None:
            # Generate new ticket ID with timestamp (format: T + timestamp)
            self.ticket_id = f"T{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}"
            if hasattr(st, "write"):
                st.write(
                    f"🔍 ITTicket.save() - Generated new ticket_id: {self.ticket_id}"
                )
        else:
            # Convert to string and check if it's empty or invalid
            ticket_id_str = str(self.ticket_id).strip()
            if (
                ticket_id_str == ""
                or ticket_id_str.lower() == "none"
                or ticket_id_str.lower() == "nan"
            ):
                # Generate new ID if provided value is invalid
                self.ticket_id = f"T{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}"
                if hasattr(st, "write"):
                    st.write(
                        f"🔍 ITTicket.save() - Original was empty/none/nan, generated: {self.ticket_id}"
                    )
            else:
                # Use provided ticket_id if valid
                self.ticket_id = ticket_id_str
                if hasattr(st, "write"):
                    st.write(
                        f"🔍 ITTicket.save() - Using provided ticket_id: {self.ticket_id}"
                    )

        # Use provided created_at if available (check for None and empty string)
        if self.created_at is not None and self.created_at != "":
            # Convert created_at to string format if it's a datetime object
            if isinstance(self.created_at, pd.Timestamp):
                created_at_value = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(self.created_at, str):
                # Already a string, use it directly (but validate it's not empty)
                created_at_value = (
                    self.created_at.strip() if self.created_at.strip() else None
                )
            else:
                created_at_value = str(self.created_at) if self.created_at else None
        else:
            created_at_value = None  # Will use CURRENT_TIMESTAMP in SQL

        # Handle resolution_time_hours - convert to numeric if it's a string
        resolution_hours = self.resolution_time_hours
        if resolution_hours is not None and resolution_hours != "":
            try:
                # Try to convert to float if it's a string
                if isinstance(resolution_hours, str):
                    resolution_hours = (
                        float(resolution_hours.strip())
                        if resolution_hours.strip()
                        else None
                    )
                elif isinstance(resolution_hours, (int, float)):
                    resolution_hours = float(resolution_hours)
            except (ValueError, AttributeError):
                resolution_hours = None
        else:
            resolution_hours = None

        query = """
            INSERT INTO it_tickets 
            (ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours)
            VALUES (?, ?, ?, ?, ?, COALESCE(?, CURRENT_TIMESTAMP), ?)
        """

        # Debug: Log what we're inserting
        import streamlit as st

        if hasattr(st, "write"):
            st.write(
                f"🔍 ITTicket.save() - Inserting ticket_id: {repr(self.ticket_id)}"
            )
            st.write(
                f"🔍 ITTicket.save() - Insert params: ticket_id={repr(self.ticket_id)}, created_at={repr(created_at_value)}, resolution_hours={repr(resolution_hours)}"
            )

        self.conn.execute(
            query,
            (
                self.ticket_id,
                self.priority,
                self.description,
                self.status,
                self.assigned_to,
                created_at_value,
                resolution_hours,
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
