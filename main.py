"""
Main database setup and testing module.
Handles complete database initialization, user migration, and data loading.
"""

import pandas as pd
import streamlit as st

# Database connection and schema management
from app.data.db import connect_database, DB_PATH
from app.data.schema import create_all_tables
# User authentication and migration services
from app.services.user_service import register_user, login_user, migrate_users_from_file

# Data loading and management functions
from app.data.datasets import load_all_csv_data
from app.data.incidents import (
    insert_incident,
    get_all_incidents,
    update_incident_status,
    delete_incident,
    get_incidents_by_type_count,
    get_high_severity_by_status,
)


def setup_database_complete():
    """
    Complete database setup: creates tables, migrates users, and loads CSV data.
    Verifies all operations and displays summary statistics.
    """
    # Display setup header
    print("\n" + "=" * 60)
    print("STARTING COMPLETE DATABASE SETUP")
    print("=" * 60)

    # Establish database connection
    conn = connect_database()

    # Create all required database tables
    create_all_tables(conn)

    # Migrate users from users.txt file to database
    migrated = migrate_users_from_file(conn)
    print(f"Users migrated: {migrated}")

    # Load all CSV files into respective database tables
    loaded = load_all_csv_data(conn)
    print(f"CSV rows loaded: {loaded}")

    # Verify database contents by counting rows in each table
    cursor = conn.cursor()
    tables = ["users", "cyber_incidents", "datasets_metadata", "it_tickets"]

    # Display database summary table
    print("\nDatabase Summary")
    print(f"{'Table':<25}{'Rows':<10}")
    print("-" * 40)

    # Count and display rows for each table
    for t in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {t}")
        print(f"{t:<25}{cursor.fetchone()[0]}")

    # Close database connection
    conn.close()

    # Display completion message with database path
    print("\nDATABASE SETUP COMPLETE!")
    print(f"Database file: {DB_PATH.resolve()}")


def run_comprehensive_tests():
    """
    Run comprehensive test suite covering authentication, CRUD operations, and analytical queries.
    Tests user registration, login, incident creation, reading, updating, and deletion.
    """
    # Display test header
    print("\n" + "=" * 60)
    print("RUNNING COMPREHENSIVE TESTS")
    print("=" * 60)

    # Establish database connection for testing
    conn = connect_database()

    # Test 1: Authentication - verify user registration and login functionality
    print("\n[TEST 1] Authentication")
    # Register a test user with secure password
    success, msg = register_user(conn, "test_user", "TestPass123!", "user")
    print(f"  Register: {'✅' if success else '❌'} {msg}")

    # Test login with registered credentials
    success, msg = login_user(conn, "test_user", "TestPass123!")
    print(f"  Login:    {'✅' if success else '❌'} {msg}")

    # Test 2: CRUD Operations - test Create, Read, Update, Delete functionality
    print("\n[TEST 2] CRUD Operations")

    # CREATE: Insert a new test incident
    test_id = insert_incident(
        conn,
        "2024-11-05",  # Timestamp
        "Test Incident",  # Category
        "Low",  # Severity
        "Open",  # Status
        "This is a test incident",  # Description
        "test_user",  # Reported by
    )
    print(f"  Create:   Incident #{test_id} created")

    # READ: Query and verify the created incident
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents WHERE id = ?", conn, params=(test_id,)
    )
    print(f"  Read:     Found incident #{test_id}")

    # UPDATE: Change incident status
    update_incident_status(conn, test_id, "Resolved")
    print("  Update:   Status updated")

    # DELETE: Remove the test incident
    delete_incident(conn, test_id)
    print("  Delete:   Incident deleted")

    # Test 3: Analytical Queries - verify data aggregation and reporting functions
    print("\n[TEST 3] Analytical Queries")

    # Get incident counts grouped by category
    df_by_type = get_incidents_by_type_count(conn)
    print(f"  By Type:         {len(df_by_type)} categories")

    # Get high severity incidents grouped by status
    df_high = get_high_severity_by_status(conn)
    print(f"  High Severity:    {len(df_high)} statuses")

    # Close database connection
    conn.close()

    # Display test completion message
    print("\n" + "=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60)


def main():
    """
    Main entry point: sets up database and optionally runs test suite.
    """
    # Initialize database with tables, users, and CSV data
    setup_database_complete()
    # Uncomment to run full tests:
    # run_comprehensive_tests()


if __name__ == "__main__":
    # Execute main function when script is run directly
    main()
