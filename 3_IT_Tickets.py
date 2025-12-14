import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path
from streamlit.components.v1 import html

# Make sure Python can find the 'app' folder BEFORE importing from it
sys.path.append(str(Path(__file__).resolve().parent.parent))
from app.components.sidebar import render_sidebar
from app.theme.dashboard_effects import apply_dashboard_effects

apply_dashboard_effects()
render_sidebar()

# ==============================
# CUSTOM "GAMING" FONTS + CARD STYLING
# ==============================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&display=swap');

    /* Main titles with neon glow */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5 {
        font-family: 'Orbitron', sans-serif;
        color: #ffffff;
        text-shadow: 0 0 5px #ff33ff, 0 0 10px #ff33ff, 0 0 20px #ff33ff, 0 0 30px #bb00ff;
        font-size: 33px;
    }

    /* Normal text */
    .stApp p, .stApp label, .stApp div {
        font-family: 'Orbitron', sans-serif;
        color: #e0e0e0;
    }

    /* KPI Cards */
    .metric-card {
        font-family: 'Orbitron', sans-serif;
        background: rgba(20,0,30,0.6);
        border-radius: 12px;
        padding: 25px 20px;
        color: #ffffff;
        text-align: center;
        box-shadow: 0 0 15px rgba(255,0,255,0.4);
        transition: 0.3s;
        min-width: 240px;
        margin-right: 15px;   /* horizontal space between cards */
        margin-bottom: 20px;  /* vertical space */
        display: inline-block; /* keep cards inline in columns */
    }
    .metric-card:hover {
        box-shadow: 0 0 25px rgba(255,0,255,0.8);
        transform: scale(1.05);
    }

    /* Buttons */
    .stButton>button {
        font-family: 'Orbitron', sans-serif;
        font-weight: bold;
        color: #ffffff;
        text-shadow: 0 0 3px #ff00ff;
    }

    /* Table headers */
    .stDataFrame th {
        font-family: 'Orbitron', sans-serif;
        color: #ffffff;
        text-shadow: 0 0 2px #ff33ff;
    }

    /* Sidebar text */
    .css-1d391kg p, .css-1d391kg label {
        font-family: 'Orbitron', sans-serif;
        color: #ff33ff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =====================================================
# ACCESS CONTROL + REDIRECT TO LOGIN
# =====================================================
st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("username", None)
st.session_state.setdefault("role", None)

if not st.session_state.logged_in:
    st.switch_page("pages/Close.py")

role = (st.session_state.role or "").strip().lower()
if role != "it":
    st.error("You do not have permission to access the IT Dashboard!")
    st.stop()

username = st.session_state.get("username", "Unknown_User")
role_display = st.session_state.get("role", "Unknown_Role")

# =====================================================
# CSS & CYBER/GAMING AESTHETICS
# =====================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&display=swap');

    body {
        background: linear-gradient(135deg, #0A0016, #15002C, #230045);
        background-size: 300% 300%;
        animation: bgShift 14s ease infinite;
    }
    @keyframes bgShift {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    h1, h2, h3, h4, label, p {
        font-family: 'Orbitron', sans-serif;
        color: #EEE !important;
        text-shadow: 0 0 5px #ff33ff, 0 0 10px #ff33ff;
    }

    /* Glass cards */
    .glass-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.15);
        padding: 20px;
        border-radius: 16px;
        backdrop-filter: blur(10px);
        box-shadow: 0 0 25px #00000040;
        margin-bottom: 25px;
    }

    /* KPI Metrics */
    .metric-card {
        background: rgba(20,0,30,0.6);
        border-radius: 12px;
        padding: 25px 20px; 
        color: #ffffff;
        text-align: center;
        box-shadow: 0 0 15px rgba(255,0,255,0.5);
        transition: 0.3s;
        min-width: 240px;
        margin-bottom: 20px;
    }
    .metric-card:hover {
        box-shadow: 0 0 25px rgba(255,0,255,0.8);
        transform: scale(1.05);
    }

    /* Buttons */
    .stButton>button {
        font-family: 'Orbitron', sans-serif;
        font-weight: bold;
        color: #ffffff;
        text-shadow: 0 0 3px #ff00ff;
        background: linear-gradient(135deg, #6D28D9, #8B5CF6);
        border-radius: 12px;
        padding: 10px 14px;
        border: none;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #5B21B6, #7C3AED);
    }

    /* Table headers */
    .stDataFrame th {
        font-family: 'Orbitron', sans-serif;
        color: #ffffff;
        text-shadow: 0 0 2px #ff33ff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =====================================================
# HEADER WITH TSParticles
# =====================================================
html(
    f"""
    <div style="position: relative; text-align: center; height: 220px; margin-bottom: 30px;">
        <!-- Import Orbitron font -->
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&display=swap" rel="stylesheet">
        <div id="holoSphere" style="
            position: absolute;
            top: 35%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 350px;
            height: 350px;
            z-index: 1;
        "></div>

        <h1 style="
            position: relative;
            z-index: 2;
            font-family: 'Orbitron', sans-serif;
            color: #ffffff;
            text-shadow: 0 0 5px #ff33ff, 0 0 10px #ff33ff, 0 0 20px #ff33ff, 0 0 30px #bb00ff;
            font-size: 50px;
            margin: 0;
            padding-top: 40px;
        ">
            💻 IT Tickets Dashboard
        </h1>

        <p style="
            position: relative;
            z-index: 2;
            font-family: 'Orbitron', sans-serif;
            color: #e0e0e0;
            font-size: 16px;
            margin-top: 5px;
        ">
            Logged in as <strong>{username}</strong> ({role_display})
        </p>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/tsparticles@2.11.1/tsparticles.bundle.min.js"></script>
    <script>
    tsParticles.load("holoSphere", {{
        fullScreen: false,
        background: {{ color: "transparent" }},
        interactivity: {{
            events: {{
                onHover: {{ enable: true, mode: "repulse" }},
                onClick: {{ enable: true, mode: "push" }}
            }},
            modes: {{
                repulse: {{ distance: 120, duration: 0.6 }},
                push: {{ quantity: 4 }}
            }}
        }},
        particles: {{
            number: {{ value: 55 }},
            size: {{ value: {{ min: 2, max: 5 }} }},
            color: {{ value: ["#bb00ff", "#ff33ff"] }},
            links: {{
                enable: true,
                distance: 85,
                color: "#d400ff",
                opacity: 0.35,
                width: 1.2
            }},
            move: {{ enable: true, speed: 1.3 }}
        }}
    }});
    </script>
    """,
    height=300,
)

# =====================================================
# DATABASE
# =====================================================
from app.data.db import connect_database
from app.data.tickets import (
    insert_ticket,
    get_all_tickets,
)

DB_PATH = Path("DATA/intelligence_platform.db")
conn = connect_database(DB_PATH)

# =====================================================
# LOAD DATA
# =====================================================
df = get_all_tickets(conn)
# Don't convert ticket_id to numeric - it may contain alphanumeric values like "T200"
# Instead, sort by ticket_id as string, but handle mixed types gracefully
# Convert to string first, then sort
df["ticket_id"] = df["ticket_id"].astype(str)
df = df.sort_values(by="ticket_id", ascending=True).reset_index(drop=True)

# =====================================================
# FILTER PANEL
# =====================================================
with st.container():
    with st.expander("🔍 Filters", expanded=False):
        colA, colB, colC, colD = st.columns(4)

        with colA:
            priority_filter = st.multiselect(
                "Priority",
                sorted(df["priority"].dropna().unique().tolist()),
                default=None,
            )
        with colB:
            status_filter = st.multiselect(
                "Status",
                sorted(df["status"].dropna().unique().tolist()),
                default=None,
            )
        with colC:
            assigned_filter = st.multiselect(
                "Assigned To",
                sorted(df["assigned_to"].dropna().unique().tolist()),
                default=None,
            )
        with colD:
            date_filter = st.date_input("Date Range", [])

# =====================================================
# APPLY FILTERS
# =====================================================
filtered_df = df.copy()
if priority_filter:
    filtered_df = filtered_df[filtered_df["priority"].isin(priority_filter)]
if status_filter:
    filtered_df = filtered_df[filtered_df["status"].isin(status_filter)]
if assigned_filter:
    filtered_df = filtered_df[filtered_df["assigned_to"].isin(assigned_filter)]
# Convert created_at to datetime, handling invalid values gracefully
if "created_at" in filtered_df.columns:
    filtered_df["created_at"] = pd.to_datetime(
        filtered_df["created_at"], errors="coerce"
    )
if len(date_filter) == 2:
    start, end = date_filter
    # Filter by date, excluding rows with invalid dates (NaT)
    filtered_df = filtered_df[
        (filtered_df["created_at"].notna())
        & (filtered_df["created_at"] >= pd.to_datetime(start))
        & (filtered_df["created_at"] <= pd.to_datetime(end))
    ]

# =====================================================
# DATA MANAGEMENT & AI ASSISTANT
# =====================================================
from app.components.data_manager import DataManager
from app.services.ai_assistant import ai_assistant

# Initialize data manager - get expected columns from actual data
if not df.empty:
    expected_columns = list(df.columns)
else:
    expected_columns = [
        "ticket_id",
        "priority",
        "description",
        "status",
        "assigned_to",
        "created_at",
        "resolution_time_hours",
        "inserted_at",  # Include inserted_at if it exists in the database
    ]


# Helper function to insert ticket from row dict
def insert_ticket_from_row(conn, **row_dict):
    """Insert ticket from row dictionary."""
    from app.data.tickets import ITTicket

    # Debug: Log what we received
    st.write(
        f"🔍 insert_ticket_from_row() - Received row_dict keys: {list(row_dict.keys())}"
    )
    st.write(
        f"🔍 insert_ticket_from_row() - ticket_id value: {repr(row_dict.get('ticket_id'))} (type: {type(row_dict.get('ticket_id')).__name__})"
    )

    ticket = ITTicket(
        conn=conn,
        ticket_id=row_dict.get("ticket_id"),
        priority=row_dict.get("priority"),
        description=row_dict.get("description"),
        status=row_dict.get("status"),
        assigned_to=row_dict.get("assigned_to"),
        created_at=row_dict.get("created_at"),
        resolution_time_hours=row_dict.get("resolution_time_hours"),
    )
    return ticket.save()


data_manager = DataManager(
    "it_tickets", expected_columns, conn=conn, insert_func=insert_ticket_from_row
)

# Get all data sources
matching_data = data_manager.get_matching_data()
unmatching_data = data_manager.get_unmatching_data()
manual_data = data_manager.get_manual_data()

# IMPORTANT: Combine with FULL data (not filtered_df) first, so manual rows are included
# Then apply filters to the combined dataset
combined_data = data_manager.combine_with_original(df)

# Parse created_at in combined data (for manual/matching data that might not be parsed)
if "created_at" in combined_data.columns:
    combined_data["created_at"] = pd.to_datetime(
        combined_data["created_at"], errors="coerce"
    )

# Apply filters to combined data (so charts include manual/uploaded data)
filtered_combined = combined_data.copy()

if priority_filter:
    filtered_combined = filtered_combined[
        filtered_combined["priority"].isin(priority_filter)
    ]

if status_filter:
    filtered_combined = filtered_combined[
        filtered_combined["status"].isin(status_filter)
    ]

if assigned_filter:
    filtered_combined = filtered_combined[
        filtered_combined["assigned_to"].isin(assigned_filter)
    ]

if len(date_filter) == 2:
    start, end = date_filter
    # Filter by date, excluding rows with invalid dates (NaT)
    filtered_combined = filtered_combined[
        (filtered_combined["created_at"].notna())
        & (filtered_combined["created_at"] >= pd.to_datetime(start))
        & (filtered_combined["created_at"] <= pd.to_datetime(end))
    ]

# Save the original filtered database data length for deletion logic
original_filtered_db_len = len(filtered_df)

# =====================================================
# DATA DISPLAY
# =====================================================
st.markdown("### 📄 Data View")

# Tabs for different data views
tab1, tab2, tab3 = st.tabs(
    [
        "📊 Combined Data",
        "❌ Unmatching Upload",
        "✏️ Manual Data",
    ]
)

with tab1:
    st.markdown("#### All Data (Original + Matching + Manual)")
    if not filtered_combined.empty:
        # Display with index for deletion - use filtered_combined to match charts
        display_data = filtered_combined.copy()
        display_data.insert(0, "Row #", range(1, len(display_data) + 1))

        # Use data editor with delete capability
        edited_df = st.data_editor(
            display_data,
            use_container_width=True,
            height=500,
            num_rows="dynamic",
            key="it_tickets_combined_editor",
            disabled=["Row #"],
            hide_index=True,
        )

        # Handle row deletions from data editor
        if "Row #" in edited_df.columns:
            edited_df_clean = edited_df.drop(columns=["Row #"]).reset_index(drop=True)
        else:
            edited_df_clean = edited_df.reset_index(drop=True)

        original_combined_len = len(filtered_combined)
        current_len = len(edited_df_clean)

        # Track processed deletions to prevent infinite rerun loop
        deletion_tracking_key = "it_tickets_deletion_tracking"
        deletion_processed_key = "it_tickets_deletion_processed"

        # Initialize tracking
        if deletion_tracking_key not in st.session_state:
            st.session_state[deletion_tracking_key] = original_combined_len
        if deletion_processed_key not in st.session_state:
            st.session_state[deletion_processed_key] = False

        # Only process deletion if:
        # 1. Current length is less than original (deletion detected)
        # 2. We haven't already processed this deletion (prevent rerun loop)
        # 3. The tracked length matches the original (ensures we're processing a new deletion)
        if (
            current_len < original_combined_len
            and not st.session_state[deletion_processed_key]
            and st.session_state[deletion_tracking_key] == original_combined_len
        ):
            # Mark deletion as being processed
            st.session_state[deletion_processed_key] = True
            st.session_state[deletion_tracking_key] = current_len

            # Rows were deleted - use primary key to identify which rows are manual/matching
            # Get list of ticket_ids from database
            db_ticket_ids = set(df["ticket_id"].astype(str).unique())

            # Separate remaining rows into database vs manual/matching
            remaining_manual_matching = []
            for idx, row in edited_df_clean.iterrows():
                ticket_id = str(row.get("ticket_id", ""))
                # If ticket_id is not in database, it's a manual/matching row
                if ticket_id not in db_ticket_ids:
                    remaining_manual_matching.append(row)

            # Convert to DataFrame
            if remaining_manual_matching:
                remaining_df = pd.DataFrame(remaining_manual_matching)
                # Put all remaining in manual (matching data is usually inserted into DB anyway)
                st.session_state["it_tickets_manual_data"] = remaining_df.reset_index(
                    drop=True
                )
                # Clear matching data
                st.session_state["it_tickets_matching_data"] = pd.DataFrame()
            else:
                # All manual/matching rows deleted
                st.session_state["it_tickets_matching_data"] = pd.DataFrame()
                st.session_state["it_tickets_manual_data"] = pd.DataFrame()

            deleted_count = original_combined_len - current_len
            st.success(f"Deleted {deleted_count} row(s).")
            # Reset flags before rerun so charts update properly
            st.session_state[deletion_processed_key] = False
            # Rerun once to refresh the display and charts
            st.rerun()
        elif current_len == original_combined_len:
            # No deletion detected - reset processing flag and update tracking
            st.session_state[deletion_processed_key] = False
            st.session_state[deletion_tracking_key] = original_combined_len
    else:
        st.info("No data available")

with tab2:
    st.markdown("#### Unmatching Uploaded Data")
    # Retrieve unmatching data fresh from session state to ensure it's up to date
    current_unmatching_data = data_manager.get_unmatching_data()
    if not current_unmatching_data.empty:
        display_unmatching = current_unmatching_data.copy()
        display_unmatching.insert(0, "Row #", range(1, len(display_unmatching) + 1))
        edited_unmatching = st.data_editor(
            display_unmatching,
            use_container_width=True,
            height=400,
            num_rows="dynamic",
            key="it_tickets_unmatching_editor",
            disabled=["Row #"],
            hide_index=True,
        )

        # Handle deletions in unmatching data
        if "Row #" in edited_unmatching.columns:
            edited_unmatching_clean = edited_unmatching.drop(
                columns=["Row #"]
            ).reset_index(drop=True)
        else:
            edited_unmatching_clean = edited_unmatching.reset_index(drop=True)

        unmatching_tracking_key = "it_tickets_unmatching_deletion_tracking"
        unmatching_processed_key = "it_tickets_unmatching_deletion_processed"

        if unmatching_tracking_key not in st.session_state:
            st.session_state[unmatching_tracking_key] = len(current_unmatching_data)
        if unmatching_processed_key not in st.session_state:
            st.session_state[unmatching_processed_key] = False

        if (
            len(edited_unmatching_clean) < len(current_unmatching_data)
            and not st.session_state[unmatching_processed_key]
            and st.session_state[unmatching_tracking_key]
            == len(current_unmatching_data)
        ):
            st.session_state[unmatching_processed_key] = True
            st.session_state[unmatching_tracking_key] = len(edited_unmatching_clean)
            st.session_state["it_tickets_unmatching_data"] = edited_unmatching_clean
            st.success(
                f"Deleted {len(current_unmatching_data) - len(edited_unmatching_clean)} row(s)."
            )
            st.rerun()
        elif len(edited_unmatching_clean) == len(current_unmatching_data):
            st.session_state[unmatching_processed_key] = False
            st.session_state[unmatching_tracking_key] = len(current_unmatching_data)

        if st.button("🗑️ Clear All Unmatching Data", key="clear_it_unmatching"):
            st.session_state["it_tickets_unmatching_data"] = pd.DataFrame()
            st.rerun()
    else:
        st.info("No unmatching uploaded data")

with tab3:
    st.markdown("#### Manually Added Data")
    if not manual_data.empty:
        display_manual = manual_data.copy()
        display_manual.insert(0, "Row #", range(1, len(display_manual) + 1))
        edited_manual = st.data_editor(
            display_manual,
            use_container_width=True,
            height=500,
            num_rows="dynamic",
            key="it_tickets_manual_editor",
            disabled=["Row #"],
            hide_index=True,
        )

        # Handle deletions in manual data
        if "Row #" in edited_manual.columns:
            edited_manual_clean = edited_manual.drop(columns=["Row #"]).reset_index(
                drop=True
            )
        else:
            edited_manual_clean = edited_manual.reset_index(drop=True)

        manual_tracking_key = "it_tickets_manual_deletion_tracking"
        manual_processed_key = "it_tickets_manual_deletion_processed"

        if manual_tracking_key not in st.session_state:
            st.session_state[manual_tracking_key] = len(manual_data)
        if manual_processed_key not in st.session_state:
            st.session_state[manual_processed_key] = False

        if (
            len(edited_manual_clean) < len(manual_data)
            and not st.session_state[manual_processed_key]
            and st.session_state[manual_tracking_key] == len(manual_data)
        ):
            st.session_state[manual_processed_key] = True
            st.session_state[manual_tracking_key] = len(edited_manual_clean)
            st.session_state["it_tickets_manual_data"] = edited_manual_clean
            st.success(f"Deleted {len(manual_data) - len(edited_manual_clean)} row(s).")
            st.rerun()
        elif len(edited_manual_clean) == len(manual_data):
            st.session_state[manual_processed_key] = False
            st.session_state[manual_tracking_key] = len(manual_data)

        if st.button("🗑️ Clear All Manual Data", key="clear_it_manual"):
            st.session_state["it_tickets_manual_data"] = pd.DataFrame()
            st.rerun()
    else:
        st.info("No manually added data")

# =====================================================
# CSV UPLOAD & MANUAL ENTRY SECTION
# =====================================================
st.markdown("---")
st.markdown("### 📤 Upload CSV or Add Data Manually")

upload_col1, upload_col2 = st.columns([1, 1])

with upload_col1:
    st.markdown("#### 📁 Upload CSV File")
    uploaded_file = st.file_uploader(
        "Choose CSV file", type="csv", key="it_tickets_csv_upload"
    )

    # Track processed files to prevent infinite rerun loop
    processed_files_key = "it_tickets_processed_files"
    if processed_files_key not in st.session_state:
        st.session_state[processed_files_key] = set()

    # Track if we're currently processing to prevent concurrent processing
    processing_key = "it_tickets_processing"
    if processing_key not in st.session_state:
        st.session_state[processing_key] = False

    # Safety: Reset processing flag if no file is being uploaded (prevents stuck state)
    if uploaded_file is None and st.session_state.get(processing_key, False):
        st.session_state[processing_key] = False

    if uploaded_file is not None:
        # Create unique identifier for this file (name + size)
        file_id = f"{uploaded_file.name}_{uploaded_file.size}"

        # Only process if this file hasn't been processed yet and we're not already processing
        if (
            file_id not in st.session_state[processed_files_key]
            and not st.session_state[processing_key]
        ):
            # Mark as processing to prevent concurrent runs
            st.session_state[processing_key] = True

            # Show progress indicator
            progress_bar = st.progress(0)
            status_text = st.empty()
            status_text.info("⏳ Processing CSV file...")

            try:
                success, message = data_manager.handle_csv_upload(uploaded_file)
                progress_bar.progress(100)
                status_text.empty()

                if success:
                    # Mark file as processed
                    st.session_state[processed_files_key].add(file_id)
                    st.success(message)
                    # Rerun if data was inserted OR if unmatching data was added
                    if (
                        "inserted" in message.lower() and "0" not in message
                    ) or "unmatching data" in message.lower():
                        # Clear processing flag BEFORE rerun to prevent stuck state
                        st.session_state[processing_key] = False
                        st.rerun()
                    else:
                        # Clear processing flag if no rerun needed
                        st.session_state[processing_key] = False
                        # No data was inserted, just show message and stop
                        st.info(
                            "No new data was inserted. Check the message above for details."
                        )
                else:
                    st.error(message)
                    # Clear processing flag
                    st.session_state[processing_key] = False
                    # Don't mark as processed if it failed completely
            except Exception as e:
                progress_bar.empty()
                status_text.empty()
                st.error(f"Error processing file: {str(e)[:200]}")
                # Show full error for debugging
                import traceback

                st.code(traceback.format_exc())
                # Clear processing flag
                st.session_state[processing_key] = False
                # Don't mark as processed on exception
        elif file_id in st.session_state[processed_files_key]:
            # File already processed, show info message
            st.info("File already processed. Upload a new file to add more data.")
            if st.button("🔄 Clear processed files list", key="clear_processed_it"):
                st.session_state[processed_files_key] = set()
                st.rerun()
        elif st.session_state[processing_key]:
            # Currently processing, show loading message
            st.info("⏳ Processing file... Please wait.")
            # Add a button to reset stuck processing flag (safety mechanism)
            if st.button("🔄 Reset Processing (if stuck)", key="reset_processing_it"):
                st.session_state[processing_key] = False
                st.rerun()

# Create a new layout: CSV on left, Chatbox on right, Manual entry below
upload_col2a, upload_col2b = st.columns(2)

with upload_col2a:
    # Draggable Chatbox (Simple AI - No API Required)
    from app.components.draggable_chatbox import draggable_chatbox

    # Get fresh unmatching data each time (in case new data was added)
    current_unmatching_data = data_manager.get_unmatching_data()

    draggable_chatbox(
        title="Simple AI Assistant",
        context_df=filtered_combined,
        role_hint="it_ticket",
        unmatching_df=current_unmatching_data,
    )

with upload_col2b:
    st.markdown("#### ✏️ Add Row Manually")
    with st.form("it_tickets_manual_form"):
        manual_ticket_id = st.text_input(
            "Ticket ID (optional - auto-generated if empty)"
        )
        manual_priority = st.selectbox(
            "Priority", ["Low", "Medium", "High", "Critical"]
        )
        manual_description = st.text_area("Description")
        manual_status = st.selectbox("Status", ["Open", "In Progress", "Resolved"])
        manual_assigned_to = st.text_input("Assigned To", st.session_state.username)
        manual_resolution_time = st.number_input(
            "Resolution Time (hours)", min_value=0.0, value=0.0, step=0.1
        )

        if st.form_submit_button("Add Row"):
            # ALWAYS use current timestamp - ignore user input to guarantee it's never None
            final_timestamp = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            row_data = {
                "ticket_id": (
                    manual_ticket_id
                    if manual_ticket_id
                    else f"T{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}"
                ),
                "priority": manual_priority,
                "description": manual_description if manual_description else "",
                "status": manual_status,
                "assigned_to": manual_assigned_to,
                "created_at": final_timestamp,  # Always current time - never None
                "resolution_time_hours": manual_resolution_time,
            }
            if data_manager.add_manual_row(row_data):
                st.success("Row added successfully!")
                st.rerun()

# =====================================================
# KPI CARDS
# =====================================================
st.markdown("## 📊 Analytics")
c1, c2, c3 = st.columns([1, 1, 1], gap="large")

c1.markdown(
    f"""
<div class="metric-card">
    <h3>Total Tickets</h3>
    <div class="metric-value">{len(filtered_combined)}</div>
</div>
""",
    unsafe_allow_html=True,
)

c2.markdown(
    f"""
<div class="metric-card">
    <h3>Open Tickets</h3>
    <div class="metric-value">{(filtered_combined['status']=='Open').sum()}</div>
</div>
""",
    unsafe_allow_html=True,
)

c3.markdown(
    f"""
<div class="metric-card">
    <h3>Avg Resolution (hrs)</h3>
    <div class="metric-value">{round(filtered_combined['resolution_time_hours'].mean(),2) if not filtered_combined.empty else 0}</div>
</div>
""",
    unsafe_allow_html=True,
)

# =====================================================
# CHARTS - ULTRA NEON / HIGH VISIBILITY
# =====================================================
import plotly.graph_objects as go

# Neon color palette
neon_colors = ["#FF00FF", "#BB00FF", "#FF33FF", "#FF66FF", "#D400FF"]

# ----------------- Pie chart - Status -----------------
status_counts = filtered_combined["status"].value_counts()
fig_status = go.Figure(
    go.Pie(
        labels=status_counts.index,
        values=status_counts.values,
        hole=0.3,
        marker=dict(
            colors=neon_colors[: len(status_counts)],
            line=dict(color="#0A0016", width=3),
        ),
        textinfo="label+percent",
        hoverinfo="label+value+percent",
        pull=[0.1 if i == status_counts.idxmax() else 0 for i in status_counts.index],
    )
)
fig_status.update_layout(
    title=dict(
        text="Ticket Status Breakdown",
        font=dict(family="Orbitron", size=26, color="#FF33FF"),
    ),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    legend=dict(font=dict(family="Orbitron", color="#FFFFFF", size=14)),
)
st.plotly_chart(fig_status, use_container_width=True)

# ----------------- Bar chart - Priority -----------------
priority_counts = filtered_combined.groupby("priority").size().reset_index(name="count")
fig_priority = go.Figure()
for idx, row in priority_counts.iterrows():
    fig_priority.add_trace(
        go.Bar(
            x=[row["priority"]],
            y=[row["count"]],
            marker=dict(
                color=neon_colors[idx % len(neon_colors)],
                line=dict(color="#FFFFFF", width=2),
                opacity=0.9,
            ),
            hovertemplate=f"<b>{row['priority']}</b>: {row['count']} tickets<extra></extra>",
        )
    )
fig_priority.update_layout(
    title=dict(
        text="Ticket Priority Levels",
        font=dict(family="Orbitron", size=26, color="#FF33FF"),
    ),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis_title=None,
    yaxis_title="Count",
    font=dict(family="Orbitron", color="#FFFFFF"),
)
st.plotly_chart(fig_priority, use_container_width=True)

# ----------------- Line chart - Tickets over time -----------------
time_counts = (
    filtered_combined.groupby(filtered_combined["created_at"].dt.date)
    .size()
    .reset_index(name="count")
)
fig_time = go.Figure()
fig_time.add_trace(
    go.Scatter(
        x=time_counts["created_at"],
        y=time_counts["count"],
        mode="lines+markers",
        line=dict(color="#FF33FF", width=4, shape="spline"),
        marker=dict(size=12, color="#BB00FF", line=dict(width=2, color="#FFFFFF")),
        hovertemplate="<b>Date:</b> %{x}<br><b>Tickets:</b> %{y}<extra></extra>",
    )
)
fig_time.update_layout(
    title=dict(
        text="Tickets Over Time", font=dict(family="Orbitron", size=26, color="#FF33FF")
    ),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis_title="Date",
    yaxis_title="Tickets",
    font=dict(family="Orbitron", color="#FFFFFF"),
)
st.plotly_chart(fig_time, use_container_width=True)

# ----------------- Box plot - Resolution times -----------------
fig_box = go.Figure()
fig_box.add_trace(
    go.Box(
        y=filtered_combined["resolution_time_hours"],
        boxpoints="all",
        jitter=0.5,
        pointpos=-1.8,
        marker=dict(color="#FF33FF", size=10, line=dict(color="#FFFFFF", width=2)),
        line=dict(color="#BB00FF", width=3),
        fillcolor="rgba(255,51,255,0.25)",
        name="Resolution Time (hrs)",
    )
)
fig_box.update_layout(
    title=dict(
        text="Resolution Time Distribution",
        font=dict(family="Orbitron", size=26, color="#FF33FF"),
    ),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis_title="Hours",
    font=dict(family="Orbitron", color="#FFFFFF"),
)
st.plotly_chart(fig_box, use_container_width=True)

# =====================================================
# NEW ENHANCED CHARTS FOR IT TICKETS
# =====================================================

if not filtered_combined.empty:
    st.markdown("## 🌟 Advanced Ticket Analytics")

    # ------------------ FUNNEL CHART: Priority Flow ------------------
    priority_order = ["Low", "Medium", "High", "Critical"]
    priority_counts = filtered_combined["priority"].value_counts()
    funnel_priority = [
        priority_counts.get(pri, 0)
        for pri in priority_order
        if pri in priority_counts.index
    ]
    funnel_labels_pri = [pri for pri in priority_order if pri in priority_counts.index]

    if funnel_priority:
        fig_funnel_priority = go.Figure(
            go.Funnel(
                y=funnel_labels_pri,
                x=funnel_priority,
                textposition="inside",
                textinfo="value+percent initial",
                marker=dict(
                    color=funnel_priority,
                    colorscale=[[0, "#00ffcc"], [0.5, "#bb00ff"], [1, "#ff33ff"]],
                    line=dict(color="#ffffff", width=3),
                ),
                textfont=dict(family="Orbitron", color="#ffffff", size=14),
            )
        )
        fig_funnel_priority.update_layout(
            title=dict(
                text="🔄 Priority Flow Funnel",
                font=dict(family="Orbitron", size=32, color="#FF33FF"),
                x=0.5,
                xanchor="center",
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Orbitron", color="#FFFFFF"),
            margin=dict(t=80, b=50, l=40, r=40),
            height=500,
        )
        st.plotly_chart(
            fig_funnel_priority,
            use_container_width=True,
            config={"displayModeBar": False},
        )

    # ------------------ GAUGE: Average Resolution Time ------------------
    avg_resolution = (
        filtered_combined["resolution_time_hours"].mean()
        if not filtered_combined.empty
        else 0
    )
    max_resolution = (
        filtered_combined["resolution_time_hours"].max()
        if not filtered_combined.empty
        else 100
    )
    gauge_res_value = (
        min(avg_resolution / max_resolution * 100, 100) if max_resolution > 0 else 0
    )

    fig_gauge_res = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=gauge_res_value,
            domain={"x": [0, 1], "y": [0, 1]},
            title={
                "text": f"Avg Resolution: {avg_resolution:.1f} hrs",
                "font": {"family": "Orbitron", "size": 24, "color": "#FF33FF"},
            },
            gauge=dict(
                axis=dict(
                    range=[None, 100],
                    tickfont=dict(family="Orbitron", color="#ffffff", size=12),
                ),
                bar=dict(color="#FF33FF"),
                steps=[
                    dict(range=[0, 33], color="rgba(0,255,204,0.3)"),
                    dict(range=[33, 66], color="rgba(187,0,255,0.3)"),
                    dict(range=[66, 100], color="rgba(255,51,255,0.3)"),
                ],
                threshold=dict(
                    line=dict(color="#ffffff", width=4),
                    thickness=0.75,
                    value=gauge_res_value,
                ),
            ),
            number=dict(font=dict(family="Orbitron", color="#ffffff", size=40)),
        )
    )
    fig_gauge_res.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Orbitron", color="#ffffff"),
        height=400,
    )
    st.plotly_chart(
        fig_gauge_res, use_container_width=True, config={"displayModeBar": False}
    )

    # ------------------ RADAR CHART: Multi-Dimensional Analysis ------------------
    if (
        "assigned_to" in filtered_combined.columns
        and "priority" in filtered_combined.columns
    ):
        radar_data = (
            filtered_combined.groupby(["assigned_to", "priority"])
            .size()
            .reset_index(name="count")
        )
        if not radar_data.empty:
            top_assignees = (
                filtered_combined["assigned_to"].value_counts().head(5).index.tolist()
            )
            priority_levels = ["Low", "Medium", "High", "Critical"]

            fig_radar = go.Figure()
            for assignee in top_assignees:
                assignee_data = radar_data[radar_data["assigned_to"] == assignee]
                values = [
                    assignee_data[assignee_data["priority"] == p]["count"].sum()
                    for p in priority_levels
                ]
                fig_radar.add_trace(
                    go.Scatterpolar(
                        r=values,
                        theta=priority_levels,
                        fill="toself",
                        name=assignee,
                        line=dict(
                            color=neon_colors[
                                top_assignees.index(assignee) % len(neon_colors)
                            ],
                            width=3,
                        ),
                    )
                )

            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[
                            0,
                            max(radar_data["count"]) if not radar_data.empty else 10,
                        ],
                        tickfont=dict(family="Orbitron", color="#ffffff", size=10),
                    ),
                    angularaxis=dict(
                        tickfont=dict(family="Orbitron", color="#ffffff", size=12),
                    ),
                    bgcolor="rgba(0,0,0,0)",
                ),
                title=dict(
                    text="📡 Priority Distribution by Assignee",
                    font=dict(family="Orbitron", size=32, color="#FF33FF"),
                    x=0.5,
                    xanchor="center",
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                legend=dict(
                    font=dict(family="Orbitron", color="#ffffff", size=12),
                    bgcolor="rgba(0,0,0,0.5)",
                    bordercolor="#FF33FF",
                    borderwidth=2,
                ),
                margin=dict(t=80, b=20, l=20, r=20),
                height=600,
            )
            st.plotly_chart(
                fig_radar, use_container_width=True, config={"displayModeBar": False}
            )

    # ------------------ WATERFALL CHART: Status Changes ------------------
    status_order_waterfall = ["Open", "In Progress", "Resolved"]
    status_counts_waterfall = filtered_combined["status"].value_counts()
    waterfall_values = []
    waterfall_labels = []
    cumulative = 0

    for status in status_order_waterfall:
        if status in status_counts_waterfall.index:
            value = status_counts_waterfall[status]
            waterfall_values.append(value)
            waterfall_labels.append(status)

    if waterfall_values:
        fig_waterfall = go.Figure(
            go.Waterfall(
                orientation="v",
                measure=["relative"] * len(waterfall_labels),
                x=waterfall_labels,
                textposition="outside",
                text=waterfall_values,
                y=waterfall_values,
                connector={"line": {"color": "#ffffff", "width": 2}},
                increasing={
                    "marker": {
                        "color": "#00ffcc",
                        "line": {"color": "#ffffff", "width": 3},
                    }
                },
                decreasing={
                    "marker": {
                        "color": "#bb00ff",
                        "line": {"color": "#ffffff", "width": 3},
                    }
                },
                totals={
                    "marker": {
                        "color": "#ff33ff",
                        "line": {"color": "#ffffff", "width": 3},
                    }
                },
                textfont=dict(family="Orbitron", color="#ffffff", size=14),
            )
        )
        fig_waterfall.update_layout(
            title=dict(
                text="💧 Status Waterfall",
                font=dict(family="Orbitron", size=32, color="#FF33FF"),
                x=0.5,
                xanchor="center",
            ),
            xaxis=dict(
                title=dict(
                    text="Status",
                    font=dict(family="Orbitron", color="#ffffff", size=16),
                ),
                tickfont=dict(family="Orbitron", color="#ffffff", size=12),
                linecolor="#FF33FF",
                linewidth=2,
            ),
            yaxis=dict(
                title=dict(
                    text="Count", font=dict(family="Orbitron", color="#ffffff", size=16)
                ),
                tickfont=dict(family="Orbitron", color="#ffffff", size=12),
                showgrid=True,
                gridcolor="rgba(255,51,255,0.2)",
                linecolor="#FF33FF",
                linewidth=2,
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=80, b=50, l=40, r=40),
            height=500,
        )
        st.plotly_chart(
            fig_waterfall, use_container_width=True, config={"displayModeBar": False}
        )


# =====================================================
# AI ASSISTANTS (Below all charts)
# =====================================================
st.markdown("---")
st.markdown("## 🤖 AI Assistants")

# Full width Premium AI (Simple AI has been moved above)
st.markdown("### 🌐 Premium AI (Gemini API)")
try:
    from app.services.ai_assistant import ai_assistant

    ai_assistant(
        title="IT Support AI Assistant",
        context_df=filtered_combined,  # Use filtered combined data
        role_hint="it_ticket",
        primary_key_name="ticket_id",
    )
except Exception as e:
    st.error(f"⚠️ Premium AI unavailable: {str(e)[:100]}")
    st.info("💡 Try using the Simple AI Assistant above!")
