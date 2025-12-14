"""
Data Manager Component Module
Handles CSV file uploads, manual data entry, column validation, and database insertion.
Manages three data categories: matching, unmatching, and manually entered data.
"""

import streamlit as st
import pandas as pd
from typing import Tuple, Optional


class DataManager:
    """
    Manages CSV upload, manual entry, and data deletion.
    Validates column structure, handles database insertion, and maintains session state.
    """

    def __init__(
        self, key_prefix: str, expected_columns: list, conn=None, insert_func=None
    ):
        """
        Initialize DataManager with column validation and database insertion support.

        Args:
            key_prefix: Prefix for session state keys (ensures uniqueness)
            expected_columns: List of expected column names for validation
            conn: Database connection (optional, for inserting matching data)
            insert_func: Function to insert rows into database (optional)
        """
        self.key_prefix = key_prefix
        self.expected_columns = expected_columns  # Required columns for validation
        self.conn = conn  # Database connection for direct insertion
        self.insert_func = insert_func  # Function to insert data into database
        # Create unique session state keys for each data category
        self.matching_key = f"{key_prefix}_matching_data"
        self.unmatching_key = f"{key_prefix}_unmatching_data"
        self.manual_key = f"{key_prefix}_manual_data"

        # Initialize session state DataFrames for each data category
        if self.matching_key not in st.session_state:
            st.session_state[self.matching_key] = pd.DataFrame()

        if self.unmatching_key not in st.session_state:
            st.session_state[self.unmatching_key] = pd.DataFrame()

        if self.manual_key not in st.session_state:
            st.session_state[self.manual_key] = pd.DataFrame()

    def check_columns_match(self, df: pd.DataFrame) -> bool:
        """
        Check if uploaded CSV columns match expected columns.
        Performs case-insensitive comparison with whitespace normalization.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            bool: True if columns match, False otherwise
        """
        # Return False if DataFrame is empty
        if df.empty:
            return False

        # Normalize column names (case-insensitive, strip whitespace)
        df_cols = [col.strip().lower() for col in df.columns]
        expected_cols = [col.strip().lower() for col in self.expected_columns]

        # Compare sets to check if all columns match (order-independent)
        return set(df_cols) == set(expected_cols)

    def _read_csv_file(self, uploaded_file) -> pd.DataFrame:
        """Read CSV file with proper type handling for ID columns."""
        id_columns = ["ticket_id", "incident_id", "dataset_id"]
        dtype_dict = {col: str for col in id_columns if col in self.expected_columns}

        if dtype_dict:
            return pd.read_csv(uploaded_file, dtype=dtype_dict)
        return pd.read_csv(uploaded_file)

    def _normalize_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalize column names to match expected columns (case-insensitive)."""
        column_mapping = {}
        for col in df.columns:
            for exp_col in self.expected_columns:
                if col.strip().lower() == exp_col.strip().lower():
                    column_mapping[col] = exp_col
                    break

        if column_mapping:
            return df.rename(columns=column_mapping)
        return df

    def _convert_row_to_dict(self, row: pd.Series) -> dict:
        """Convert pandas row to dictionary with proper type conversion."""
        row_dict = row.to_dict()

        # Ensure all expected columns are present
        for col in self.expected_columns:
            if col not in row_dict:
                row_dict[col] = None

        # Convert pandas/numpy types to Python native types
        for key, value in row_dict.items():
            if value is None:
                continue

            if pd.isna(value):
                row_dict[key] = None
            elif isinstance(value, pd.Timestamp):
                row_dict[key] = value.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(value, pd.Timedelta):
                row_dict[key] = str(value)
            elif hasattr(value, "dtype"):
                if "int" in str(value.dtype):
                    row_dict[key] = int(value)
                elif "float" in str(value.dtype):
                    row_dict[key] = float(value)
                else:
                    row_dict[key] = value.item() if hasattr(value, "item") else value
            elif isinstance(value, (int, float, str)):
                row_dict[key] = value
            else:
                row_dict[key] = str(value) if value is not None else None

        return row_dict

    def _is_duplicate_error(self, error_str: str) -> bool:
        """Check if error is a duplicate/UNIQUE constraint violation."""
        return (
            "UNIQUE constraint" in error_str
            or "duplicate" in error_str.lower()
            or "UNIQUE constraint failed" in error_str
        )

    def _get_primary_key_field(self, row_dict: dict) -> Optional[Tuple[str, str]]:
        """Get primary key field name and value from row dict."""
        for col in ["incident_id", "ticket_id", "dataset_id"]:
            if col in row_dict and row_dict[col] is not None:
                return col, row_dict[col]
        return None, None

    def _insert_matching_rows_to_db(self, df: pd.DataFrame) -> Tuple[bool, str]:
        """Insert matching CSV rows into database."""
        inserted_count = 0
        error_count = 0
        skipped_count = 0

        df_normalized = self._normalize_column_names(df)

        for idx, row in df_normalized.iterrows():
            try:
                row_dict = self._convert_row_to_dict(row)

                # Debug first row
                if idx == df_normalized.index[0]:
                    self._debug_first_row(row, row_dict)

                try:
                    self.insert_func(self.conn, **row_dict)
                    inserted_count += 1
                except Exception as insert_error:
                    raise insert_error

            except Exception as e:
                error_str = str(e)
                if self._is_duplicate_error(error_str):
                    skipped_count += 1
                    pk_field, pk_value = self._get_primary_key_field(row_dict)
                    if skipped_count <= 3:
                        msg = (
                            f"Row {idx + 1} skipped: {pk_field} '{pk_value}' already exists"
                            if pk_field
                            else f"Row {idx + 1} skipped: Duplicate entry already exists"
                        )
                        st.warning(msg)
                else:
                    error_count += 1
                    if error_count <= 3:
                        st.error(f"Error inserting row {idx + 1}: {str(e)[:200]}")
                        if error_count == 1:
                            import traceback

                            st.code(traceback.format_exc())

        return self._build_insert_result_message(
            inserted_count, skipped_count, error_count
        )

    def _debug_first_row(self, row: pd.Series, row_dict: dict):
        """Debug logging for first row insertion."""
        debug_fields = ["ticket_id", "created_at", "resolution_time_hours"]
        raw_values = {
            k: (
                row.get(k),
                type(row.get(k)).__name__ if row.get(k) is not None else "None",
            )
            for k in debug_fields
            if k in row.index
        }
        processed_values = {
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
        if processed_values:
            st.write(f"🔍 Debug - Raw CSV values: {raw_values}")
            st.write(f"🔍 Debug - Processed values: {processed_values}")

    def _build_insert_result_message(
        self, inserted: int, skipped: int, errors: int
    ) -> Tuple[bool, str]:
        """Build result message for database insertion."""
        result_parts = []
        if inserted > 0:
            result_parts.append(f"Successfully inserted {inserted} row(s)")
        if skipped > 0:
            result_parts.append(f"Skipped {skipped} duplicate(s)")
        if errors > 0:
            result_parts.append(f"{errors} error(s)")

        if inserted > 0:
            return True, ", ".join(result_parts) + "."
        elif skipped > 0 and errors == 0:
            return (
                False,
                f"All rows were skipped (duplicates). {skipped} duplicate(s) found.",
            )
        else:
            return (
                False,
                f"Failed to insert any rows. {errors} error(s), {skipped} duplicate(s).",
            )

    def _store_matching_data(self, df: pd.DataFrame) -> Tuple[bool, str]:
        """Store matching data in session state (backward compatibility)."""
        if st.session_state[self.matching_key].empty:
            st.session_state[self.matching_key] = df
        else:
            st.session_state[self.matching_key] = pd.concat(
                [st.session_state[self.matching_key], df], ignore_index=True
            )
        return True, f"Successfully added {len(df)} rows to matching data"

    def _store_unmatching_data(self, df: pd.DataFrame) -> Tuple[bool, str]:
        """Store unmatching data in session state."""
        if st.session_state[self.unmatching_key].empty:
            st.session_state[self.unmatching_key] = df
        else:
            st.session_state[self.unmatching_key] = pd.concat(
                [st.session_state[self.unmatching_key], df], ignore_index=True
            )
        return True, f"Columns don't match. Added {len(df)} rows to unmatching data"

    def handle_csv_upload(self, uploaded_file) -> Tuple[bool, str]:
        """
        Handle CSV file upload with validation and routing.
        Validates columns, routes to database or session state based on configuration.
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            tuple: (success: bool, message: str) - Upload result
        """
        # Check if file was uploaded
        if uploaded_file is None:
            return False, "No file uploaded"

        try:
            # Read CSV file with proper type handling
            df = self._read_csv_file(uploaded_file)

            # Validate file is not empty
            if df.empty:
                return False, "Uploaded CSV is empty"

            # Check if columns match expected structure
            if self.check_columns_match(df):
                # Columns match - insert into database or store in session state
                if self.conn is not None and self.insert_func is not None:
                    # Insert directly into database
                    return self._insert_matching_rows_to_db(df)
                else:
                    # Store in session state for later use
                    return self._store_matching_data(df)
            else:
                # Columns don't match - store as unmatching data for review
                return self._store_unmatching_data(df)

        except Exception as e:
            # Return error message if file reading fails
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
