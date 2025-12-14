import streamlit as st
import pandas as pd
from typing import Tuple, Optional


class DataManager:
    """Manages CSV upload, manual entry, and data deletion."""

    def __init__(
        self, key_prefix: str, expected_columns: list, conn=None, insert_func=None
    ):
        """Initialize DataManager.

        Args:
            key_prefix: Prefix for session state keys
            expected_columns: List of expected column names
            conn: Database connection (optional, for inserting matching data)
            insert_func: Function to insert rows into database (optional)
        """
        self.key_prefix = key_prefix
        self.expected_columns = expected_columns
        self.conn = conn
        self.insert_func = insert_func
        self.matching_key = f"{key_prefix}_matching_data"
        self.unmatching_key = f"{key_prefix}_unmatching_data"
        self.manual_key = f"{key_prefix}_manual_data"

        # Initialize session state
        if self.matching_key not in st.session_state:
            st.session_state[self.matching_key] = pd.DataFrame()

        if self.unmatching_key not in st.session_state:
            st.session_state[self.unmatching_key] = pd.DataFrame()

        if self.manual_key not in st.session_state:
            st.session_state[self.manual_key] = pd.DataFrame()

    def check_columns_match(self, df: pd.DataFrame) -> bool:
        """Check if uploaded CSV columns match expected columns."""
        if df.empty:
            return False

        # Normalize column names (case-insensitive, strip whitespace)
        df_cols = [col.strip().lower() for col in df.columns]
        expected_cols = [col.strip().lower() for col in self.expected_columns]

        return set(df_cols) == set(expected_cols)

    def handle_csv_upload(self, uploaded_file) -> Tuple[bool, str]:
        """Handle CSV file upload."""
        if uploaded_file is None:
            return False, "No file uploaded"

        try:
            # Read CSV with dtype=str for ID columns to prevent type inference issues
            # This ensures ticket_id, incident_id, dataset_id are read as strings
            id_columns = ["ticket_id", "incident_id", "dataset_id"]
            dtype_dict = {}
            for col in id_columns:
                if col in self.expected_columns:
                    dtype_dict[col] = str

            # Also preserve numeric columns that might be read incorrectly
            # Don't force dtype for numeric columns - let pandas infer them naturally
            # But ensure ID columns stay as strings

            # Read CSV, preserving string types for ID columns only
            if dtype_dict:
                df = pd.read_csv(uploaded_file, dtype=dtype_dict)
            else:
                df = pd.read_csv(uploaded_file)

            if df.empty:
                return False, "Uploaded CSV is empty"

            if self.check_columns_match(df):
                # Columns match - insert directly into database if connection and insert function provided
                if self.conn is not None and self.insert_func is not None:
                    inserted_count = 0
                    error_count = 0
                    skipped_count = 0

                    # Normalize column names to match expected columns (case-insensitive)
                    df_normalized = df.copy()
                    column_mapping = {}
                    for col in df.columns:
                        # Find matching expected column (case-insensitive)
                        for exp_col in self.expected_columns:
                            if col.strip().lower() == exp_col.strip().lower():
                                column_mapping[col] = exp_col
                                break

                    # Rename columns to match expected names
                    if column_mapping:
                        df_normalized = df_normalized.rename(columns=column_mapping)

                    for idx, row in df_normalized.iterrows():
                        try:
                            # Convert row to dict - keep all expected columns
                            row_dict = row.to_dict()

                            # Ensure all expected columns are present (set to None if missing)
                            for col in self.expected_columns:
                                if col not in row_dict:
                                    row_dict[col] = None

                            # Convert NaN/NaT values to None for database insertion
                            # But preserve valid values (including empty strings for some fields)
                            for key, value in row_dict.items():
                                # Skip if value is already None
                                if value is None:
                                    continue

                                if pd.isna(value):
                                    row_dict[key] = None
                                # Convert pandas types to Python native types
                                elif isinstance(value, (pd.Timestamp, pd.Timedelta)):
                                    # Convert to string format for datetime fields
                                    if isinstance(value, pd.Timestamp):
                                        row_dict[key] = value.strftime(
                                            "%Y-%m-%d %H:%M:%S"
                                        )
                                    else:
                                        row_dict[key] = str(value)
                                # Handle numpy numeric types (numpy.int64, numpy.float64, etc.)
                                elif hasattr(value, "dtype"):
                                    # Convert numpy types to Python native types
                                    if "int" in str(value.dtype):
                                        row_dict[key] = int(value)
                                    elif "float" in str(value.dtype):
                                        row_dict[key] = float(value)
                                    else:
                                        row_dict[key] = (
                                            value.item()
                                            if hasattr(value, "item")
                                            else value
                                        )
                                # Keep numeric values as-is (int, float)
                                elif isinstance(value, (int, float)):
                                    row_dict[key] = value
                                # Keep strings as-is (including empty strings)
                                elif isinstance(value, str):
                                    row_dict[key] = value
                                # For any other type, convert to string
                                else:
                                    row_dict[key] = (
                                        str(value) if value is not None else None
                                    )

                            # Debug: Log first row to see what we're passing (only for first row)
                            if idx == df_normalized.index[0]:
                                debug_fields = [
                                    "ticket_id",
                                    "created_at",
                                    "resolution_time_hours",
                                ]
                                # Also show raw row values before processing
                                raw_row_values = {
                                    k: (
                                        row.get(k),
                                        (
                                            type(row.get(k)).__name__
                                            if row.get(k) is not None
                                            else "None"
                                        ),
                                    )
                                    for k in debug_fields
                                    if k in row.index
                                }
                                debug_values = {
                                    k: (
                                        row_dict.get(k),
                                        (
                                            type(row_dict.get(k)).__name__
                                            if row_dict.get(k) is not None
                                            else "None"
                                        ),
                                    )
                                    for k in debug_fields
                                    if k in row_dict
                                }
                                if debug_values:
                                    st.write(
                                        f"🔍 Debug - Raw CSV values: {raw_row_values}"
                                    )
                                    st.write(
                                        f"🔍 Debug - Processed values: {debug_values}"
                                    )

                            # Call insert function with row data
                            try:
                                self.insert_func(self.conn, **row_dict)
                                inserted_count += 1
                            except Exception as insert_error:
                                # Re-raise to be caught by outer exception handler
                                raise insert_error
                        except Exception as e:
                            error_str = str(e)
                            # Check if it's a UNIQUE constraint violation (duplicate ID)
                            if (
                                "UNIQUE constraint" in error_str
                                or "duplicate" in error_str.lower()
                                or "UNIQUE constraint failed" in error_str
                            ):
                                skipped_count += 1
                                # Get the primary key field name for better messaging
                                pk_field = None
                                for col in ["incident_id", "ticket_id", "dataset_id"]:
                                    if col in row_dict and row_dict[col] is not None:
                                        pk_field = col
                                        pk_value = row_dict[col]
                                        break

                                if skipped_count <= 3:  # Show first 3 skipped rows
                                    if pk_field:
                                        st.warning(
                                            f"Row {idx + 1} skipped: {pk_field} '{pk_value}' already exists in database"
                                        )
                                    else:
                                        st.warning(
                                            f"Row {idx + 1} skipped: Duplicate entry already exists"
                                        )
                            else:
                                error_count += 1
                                # Show all other errors for debugging (limit to first 3 to avoid spam)
                                if error_count <= 3:
                                    error_msg = (
                                        f"Error inserting row {idx + 1}: {str(e)[:200]}"
                                    )
                                    st.error(error_msg)
                                    # Also show full traceback for first error to help debug
                                    if error_count == 1:
                                        import traceback

                                        st.code(traceback.format_exc())

                    # Build result message
                    result_parts = []
                    if inserted_count > 0:
                        result_parts.append(
                            f"Successfully inserted {inserted_count} row(s)"
                        )
                    if skipped_count > 0:
                        result_parts.append(f"Skipped {skipped_count} duplicate(s)")
                    if error_count > 0:
                        result_parts.append(f"{error_count} error(s)")

                    if inserted_count > 0:
                        message = ", ".join(result_parts) + "."
                        return True, message
                    elif skipped_count > 0 and error_count == 0:
                        return (
                            False,
                            f"All rows were skipped (duplicates). {skipped_count} duplicate(s) found.",
                        )
                    else:
                        return (
                            False,
                            f"Failed to insert any rows. {error_count} error(s), {skipped_count} duplicate(s).",
                        )
                else:
                    # No database connection - store in session state (backward compatibility)
                    if st.session_state[self.matching_key].empty:
                        st.session_state[self.matching_key] = df
                    else:
                        st.session_state[self.matching_key] = pd.concat(
                            [st.session_state[self.matching_key], df], ignore_index=True
                        )
                    return True, f"Successfully added {len(df)} rows to matching data"
            else:
                # Columns don't match - add to unmatching data
                if st.session_state[self.unmatching_key].empty:
                    st.session_state[self.unmatching_key] = df
                else:
                    st.session_state[self.unmatching_key] = pd.concat(
                        [st.session_state[self.unmatching_key], df], ignore_index=True
                    )
                return (
                    True,
                    f"Columns don't match. Added {len(df)} rows to unmatching data",
                )

        except Exception as e:
            return False, f"Error reading CSV: {str(e)}"

    def add_manual_row(self, row_data: dict) -> bool:
        """Add a manually entered row."""
        try:
            current_time = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")

            # FORCE timestamp to always be set - ALWAYS use current time, no exceptions
            if "timestamp" in self.expected_columns:
                # Always set to current timestamp, regardless of input
                row_data["timestamp"] = current_time

            # FORCE inserted_at to always be set if it's in expected columns
            if "inserted_at" in self.expected_columns:
                # Always set to current timestamp
                row_data["inserted_at"] = current_time

            # Create DataFrame from row data
            new_row = pd.DataFrame([row_data])

            # Ensure columns match expected
            for col in self.expected_columns:
                if col not in new_row.columns:
                    # For timestamp and inserted_at, always generate them
                    if col == "timestamp" or col == "inserted_at":
                        new_row[col] = current_time
                    else:
                        new_row[col] = None

            # Reorder columns to match expected
            new_row = new_row[self.expected_columns]

            # CRITICAL: Force timestamp and inserted_at to be strings and ensure they're never None
            for time_col in ["timestamp", "inserted_at"]:
                if time_col in new_row.columns:
                    # Always set to current time as a string
                    new_row[time_col] = current_time
                    # Ensure it's stored as string type
                    new_row[time_col] = new_row[time_col].astype(str)

            # Add to manual data
            if st.session_state[self.manual_key].empty:
                st.session_state[self.manual_key] = new_row
            else:
                st.session_state[self.manual_key] = pd.concat(
                    [st.session_state[self.manual_key], new_row], ignore_index=True
                )

            return True
        except Exception as e:
            st.error(f"Error adding row: {str(e)}")
            return False

    def delete_row(self, data_type: str, index: int) -> bool:
        """Delete a row from specified data type."""
        try:
            if data_type == "matching":
                if not st.session_state[self.matching_key].empty:
                    st.session_state[self.matching_key] = (
                        st.session_state[self.matching_key]
                        .drop(index)
                        .reset_index(drop=True)
                    )
                    return True
            elif data_type == "unmatching":
                if not st.session_state[self.unmatching_key].empty:
                    st.session_state[self.unmatching_key] = (
                        st.session_state[self.unmatching_key]
                        .drop(index)
                        .reset_index(drop=True)
                    )
                    return True
            elif data_type == "manual":
                if not st.session_state[self.manual_key].empty:
                    st.session_state[self.manual_key] = (
                        st.session_state[self.manual_key]
                        .drop(index)
                        .reset_index(drop=True)
                    )
                    return True

            return False
        except Exception as e:
            st.error(f"Error deleting row: {str(e)}")
            return False

    def get_matching_data(self) -> pd.DataFrame:
        """Get matching data."""
        return st.session_state[self.matching_key]

    def get_unmatching_data(self) -> pd.DataFrame:
        """Get unmatching data."""
        return st.session_state[self.unmatching_key]

    def get_manual_data(self) -> pd.DataFrame:
        """Get manually added data."""
        return st.session_state[self.manual_key]

    def get_all_data(self) -> pd.DataFrame:
        """Get all data combined (original + matching + manual)."""
        # This should be called with original data from outside
        pass

    def combine_with_original(self, original_df: pd.DataFrame) -> pd.DataFrame:
        """Combine original data with matching and manual data."""
        combined = original_df.copy()

        if not st.session_state[self.matching_key].empty:
            combined = pd.concat(
                [combined, st.session_state[self.matching_key]], ignore_index=True
            )

        if not st.session_state[self.manual_key].empty:
            combined = pd.concat(
                [combined, st.session_state[self.manual_key]], ignore_index=True
            )

        return combined
