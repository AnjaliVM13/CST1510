import sqlite3
import pandas as pd
import os
from datetime import datetime


# ============================================================
# DATASET CLASS (OOP)
# ============================================================
class Dataset:
    """Dataset class for managing dataset metadata and operations."""

    def __init__(
        self,
        conn,
        dataset_id=None,
        name=None,
        rows=None,
        columns=None,
        uploaded_by=None,
        upload_date=None,
    ):
        """Initialize a Dataset instance."""
        self.conn = conn
        self.dataset_id = dataset_id
        self.name = name
        self.rows = rows
        self.columns = columns
        self.uploaded_by = uploaded_by
        self.upload_date = upload_date

    @classmethod
    def from_db_row(cls, conn, db_row):
        """Create Dataset instance from database row."""
        if db_row is None:
            return None
        return cls(
            conn=conn,
            dataset_id=db_row[0] if len(db_row) > 0 else None,
            name=db_row[1] if len(db_row) > 1 else None,
            rows=db_row[2] if len(db_row) > 2 else None,
            columns=db_row[3] if len(db_row) > 3 else None,
            uploaded_by=db_row[4] if len(db_row) > 4 else None,
            upload_date=db_row[5] if len(db_row) > 5 else None,
        )

    def save(self):
        """Save dataset metadata to database."""
        if self.dataset_id is None:
            self.dataset_id = f"DS{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}"

        query = """
            INSERT INTO datasets_metadata
            (dataset_id, name, rows, columns, uploaded_by, upload_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """

        self.conn.execute(
            query,
            (
                self.dataset_id,
                self.name,
                self.rows,
                self.columns,
                self.uploaded_by,
                self.upload_date,
            ),
        )
        self.conn.commit()

        return self.dataset_id

    def to_dict(self):
        """Convert dataset to dictionary."""
        return {
            "dataset_id": self.dataset_id,
            "name": self.name,
            "rows": self.rows,
            "columns": self.columns,
            "uploaded_by": self.uploaded_by,
            "upload_date": self.upload_date,
        }

    @classmethod
    def get_all(cls, conn):
        """Get all datasets as DataFrame."""
        query = """
            SELECT dataset_id, name, rows, columns, uploaded_by, upload_date
            FROM datasets_metadata
            ORDER BY upload_date DESC
        """
        df = pd.read_sql_query(query, conn)
        return df

    @classmethod
    def load_csv_to_table(cls, conn, csv_path, table_name):
        """Load CSV file into a specific SQL table."""
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
            df.to_sql(name=table_name, con=conn, if_exists="append", index=False)
        except Exception as e:
            print(f"Error inserting into table '{table_name}': {e}")
            return 0

        print(f"Loaded {len(df)} rows into '{table_name}'")
        return len(df)

    @classmethod
    def load_all_csv_data(cls, conn):
        """Load all CSV files into their respective tables."""
        DATA_DIR = "DATA"

        csv_mapping = {
            "cyber_incidents": os.path.join(DATA_DIR, "cyber_incidents.csv"),
            "datasets_metadata": os.path.join(DATA_DIR, "datasets_metadata.csv"),
            "it_tickets": os.path.join(DATA_DIR, "it_tickets.csv"),
        }

        total_rows = 0
        for table, csv_path in csv_mapping.items():
            rows = cls.load_csv_to_table(conn, csv_path, table)
            total_rows += rows

        return total_rows


# ============================================================
# BACKWARD COMPATIBILITY WRAPPER FUNCTIONS
# ============================================================
def insert_dataset_metadata(conn, name, rows, columns, uploaded_by, upload_date):
    """Insert dataset metadata - backward compatibility wrapper."""
    dataset = Dataset(
        conn=conn,
        name=name,
        rows=rows,
        columns=columns,
        uploaded_by=uploaded_by,
        upload_date=upload_date,
    )
    return dataset.save()


def get_all_datasets(conn):
    """Get all datasets - backward compatibility wrapper."""
    return Dataset.get_all(conn)


def load_csv_to_table(conn, csv_path, table_name):
    """Load CSV to table - backward compatibility wrapper."""
    return Dataset.load_csv_to_table(conn, csv_path, table_name)


def load_all_csv_data(conn):
    """Load all CSV data - backward compatibility wrapper."""
    return Dataset.load_all_csv_data(conn)
