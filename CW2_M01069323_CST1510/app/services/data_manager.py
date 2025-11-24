from app.data.db import connect_database
from app.data.users import get_user_by_username, validate_login, insert_user
from app.data.incidents import (
    get_all_incidents,
    get_incidents_by_type_count,
    get_high_severity_by_status,
    insert_incident
)
from app.data.datasets import (
    insert_dataset_metadata,
    get_all_datasets
)
from app.data.tickets import (
    insert_ticket,
    get_all_tickets,
    update_ticket_status,
    get_ticket_priority_counts
)


class DataManager:
    """Unified data access layer for the AI assistant."""

    def __init__(self):
        self.conn = connect_database()

    # ---------------- USERS ----------------
    def users(self):
        return {
            "all": "Use login functions only",
        }

    # ---------------- INCIDENTS ----------------
    def incidents(self):
        return {
            "all": get_all_incidents(self.conn),
            "type_counts": get_incidents_by_type_count(self.conn),
            "high_severity_by_status": get_high_severity_by_status(self.conn),
        }

    # ---------------- DATASETS ----------------
    def datasets(self):
        return {
            "all": get_all_datasets(self.conn),
        }

    # ---------------- TICKETS ----------------
    def tickets(self):
        return {
            "all": get_all_tickets(self.conn),
            "priority_counts": get_ticket_priority_counts(self.conn),
        }

    # ---------------- EVERYTHING ----------------
    def load_all(self):
        return {
            "incidents": self.incidents(),
            "datasets": self.datasets(),
            "tickets": self.tickets(),
        }
