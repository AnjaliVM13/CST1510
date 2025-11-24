import pandas as pd

# ---------------------------------------------------------
# INSERT IT TICKET
# ---------------------------------------------------------
def insert_ticket(conn, priority, description, status, assigned_to, resolution_time_hours):
    ticket_id = f"T{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}"

    query = """
        INSERT INTO it_tickets 
        (ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours)
        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?)
    """

    conn.execute(query, (
        ticket_id,
        priority,
        description,
        status,
        assigned_to,
        resolution_time_hours
    ))
    conn.commit()

    return ticket_id


# ---------------------------------------------------------
# GET ALL TICKETS
# ---------------------------------------------------------
def get_all_tickets(conn):
    query = """
        SELECT ticket_id, priority, description, status, assigned_to, created_at, resolution_time_hours
        FROM it_tickets
        ORDER BY created_at DESC
    """
    return pd.read_sql_query(query, conn)


# ---------------------------------------------------------
# UPDATE TICKET STATUS
# ---------------------------------------------------------
def update_ticket_status(conn, ticket_id, new_status):
    query = """
        UPDATE it_tickets
        SET status = ?
        WHERE ticket_id = ?
    """

    conn.execute(query, (new_status, ticket_id))
    conn.commit()


# ---------------------------------------------------------
# ANALYTICS — TICKET COUNT BY PRIORITY
# ---------------------------------------------------------
def get_ticket_priority_counts(conn):
    query = """
        SELECT priority, COUNT(*) AS count
        FROM it_tickets
        GROUP BY priority
        ORDER BY count DESC
    """
    return pd.read_sql_query(query, conn)
