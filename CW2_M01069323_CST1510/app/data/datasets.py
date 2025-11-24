import sqlite3
import pandas as pd
import os

# ---------------------------------------------------------
# INSERT DATASET METADATA
# ---------------------------------------------------------
def insert_dataset_metadata(conn, name, rows, columns, uploaded_by, upload_date):
    """
    Insert a dataset metadata record into datasets_metadata table.
    """
    dataset_id = f"DS{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}"

    query = """
        INSERT INTO datasets_metadata
        (dataset_id, name, rows, columns, uploaded_by, upload_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """

    conn.execute(query, (dataset_id, name, rows, columns, uploaded_by, upload_date))
    conn.commit()

    return dataset_id


# ---------------------------------------------------------
# GET ALL DATASETS
# ---------------------------------------------------------
def get_all_datasets(conn):
    """
    Returns all dataset metadata as a pandas DataFrame.
    """
    query = """
        SELECT dataset_id, name, rows, columns, uploaded_by, upload_date
        FROM datasets_metadata
        ORDER BY upload_date DESC
    """
    df = pd.read_sql_query(query, conn)
    return df


# ---------------------------------------------------------
# LOAD CSV INTO A SPECIFIC SQL TABLE
# ---------------------------------------------------------
def load_csv_to_table(conn, csv_path, table_name):
    if not os.path.exists(csv_path):
        print(f"CSV not found: {csv_path}")
        return 0

    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"Error reading CSV {csv_path}: {e}")
        return 0

    if df.empty:
        print(f"CSV is empty: {csv_path}")
        return 0

    try:
        df.to_sql(name=table_name, con=conn, if_exists='append', index=False)
    except Exception as e:
        print(f"Error inserting into table '{table_name}': {e}")
        return 0

    print(f"Loaded {len(df)} rows into '{table_name}'")
    return len(df)


# ---------------------------------------------------------
# LOAD ALL CSV FILES
# ---------------------------------------------------------
def load_all_csv_data(conn):
    DATA_DIR = "DATA"

    csv_mapping = {
        "cyber_incidents": os.path.join(DATA_DIR, "cyber_incidents.csv"),
        "datasets_metadata": os.path.join(DATA_DIR, "datasets_metadata.csv"),
        "it_tickets": os.path.join(DATA_DIR, "it_tickets.csv")
    }

    total_rows = 0
    for table, csv_path in csv_mapping.items():
        rows = load_csv_to_table(conn, csv_path, table)
        total_rows += rows

    return total_rows
