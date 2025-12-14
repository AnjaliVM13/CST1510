"""
Data Manager Service Module
Provides unified data access layer for AI assistant.
Aggregates data from all database tables for comprehensive context.
"""

# Database connection
from app.data.db import connect_database
# User data access functions
from app.data.users import get_user_by_username, validate_login, insert_user
# Incident data access functions
from app.data.incidents import (
    get_all_incidents,
    get_incidents_by_type_count,
    get_high_severity_by_status,
    insert_incident
)
# Dataset data access functions
from app.data.datasets import (
    insert_dataset_metadata,
    get_all_datasets
)
# Ticket data access functions
from app.data.tickets import (
    insert_ticket,
    get_all_tickets,
    update_ticket_status,
    get_ticket_priority_counts
)


class DataManager:
    """
    Unified data access layer for the AI assistant.
    Provides centralized access to all database entities and analytics.
    """

    def __init__(self):
        """Initialize DataManager with database connection."""
        # Establish database connection
        self.conn = connect_database()

    # ---------------- USERS ----------------
    def users(self):
        """
        Get user data access information.
        Note: User operations should use dedicated login functions.
        
        Returns:
            dict: User access information
        """
        return {
            "all": "Use login functions only",
        }

    # ---------------- INCIDENTS ----------------
    def incidents(self):
        """
        Get all incident data and analytics.
        
        Returns:
            dict: Contains all incidents, type counts, and high severity by status
        """
        return {
            "all": get_all_incidents(self.conn),  # All incident records
            "type_counts": get_incidents_by_type_count(self.conn),  # Count by category
            "high_severity_by_status": get_high_severity_by_status(self.conn),  # High severity analytics
        }

    # ---------------- DATASETS ----------------
    def datasets(self):
        """
        Get all dataset metadata.
        
        Returns:
            dict: Contains all dataset records
        """
        return {
            "all": get_all_datasets(self.conn),  # All dataset metadata records
        }

    # ---------------- TICKETS ----------------
    def tickets(self):
        """
        Get all ticket data and analytics.
        
        Returns:
            dict: Contains all tickets and priority counts
        """
        return {
            "all": get_all_tickets(self.conn),  # All ticket records
            "priority_counts": get_ticket_priority_counts(self.conn),  # Count by priority
        }

    # ---------------- EVERYTHING ----------------
    def load_all(self):
        """
        Load all data from all entities for comprehensive AI context.
        
        Returns:
            dict: Contains incidents, datasets, and tickets data
        """
        return {
            "incidents": self.incidents(),  # All incident data
            "datasets": self.datasets(),  # All dataset data
            "tickets": self.tickets(),  # All ticket data
        }
