import streamlit as st
import pandas as pd
import plotly.express as px
import sys
from pathlib import Path
from streamlit.components.v1 import html

# Make sure Python can find the 'app' folder BEFORE importing from it
sys.path.append(str(Path(__file__).resolve().parent.parent))
from app.components.sidebar import render_sidebar
from app.theme.dashboard_effects import apply_dashboard_effects

apply_dashboard_effects()


# ==============================
# CUSTOM "GAMING" FONTS
# ==============================
st.markdown(
    """
    <style>
    /* Import gaming-style font (Orbitron) */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&display=swap');

    /* Apply to main titles: white text + neon pink glow */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5 {
        font-family: 'Orbitron', sans-serif;
        color: #ffffff;   /* white font */
        text-shadow: 
            0 0 5px #ff33ff, 
            0 0 10px #ff33ff, 
            0 0 20px #ff33ff,
            0 0 30px #bb00ff;
            font-size: 33px;
    }

    /* Apply to normal text */
    .stApp p, .stApp label, .stApp div {
        font-family: 'Orbitron', sans-serif;
        color: #e0e0e0;
    }

    /* Style metric cards (KPI) */
    .metric-card {
        font-family: 'Orbitron', sans-serif;
        background: rgba(20,0,30,0.6);
        border-radius: 12px;
        padding: 25px 20px; 
        color: #ffffff;
        text-align: center;
        box-shadow: 0 0 15px rgba(255,0,255,0.5);
        transition: 0.3s;
        min-width: 240px;  
        margin-bottom: 20px;   /* ← adds vertical space under each box */

    }
    .metric-card:hover {
        box-shadow: 0 0 25px rgba(255,0,255,0.8);
        transform: scale(1.05);
    }

    /* Style buttons */
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
    
    /* Maximize main content area width - use almost full screen */
    .main .block-container {
        max-width: 100% !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
    
    /* Ensure data tables use full width */
    [data-testid="stDataFrame"], [data-testid="stDataEditor"] {
        width: 100% !important;
    }
    
    /* Make columns use more space with minimal padding */
    .stColumn {
        padding-left: 0.25rem !important;
        padding-right: 0.25rem !important;
    }
    
    /* Expand column containers */
    [data-testid="column"] {
        width: 100% !important;
    }
    
    /* Ensure both columns use their allocated space properly */
    /* Streamlit handles the [4, 3] ratio naturally - CSV gets ~57%, Chatbot gets ~43% */
    </style>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# SIDEBAR
# =====================================================
from app.components.sidebar import render_sidebar

render_sidebar()

# =====================================================
# AI ASSISTANT (Original - Restored)
# =====================================================
from app.services.ai_assistant import ai_assistant

# Original AI Assistant restored - no floating icon CSS needed

# =====================================================
# ACCESS CONTROL
# =====================================================
st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("username", None)
st.session_state.setdefault("role", None)

if not st.session_state.logged_in:
    st.switch_page("pages/Close.py")

role = (st.session_state.role or "").strip().lower()
if role != "cyber":
    st.error("You do not have permission to access the Cyber Dashboard!")
    st.stop()


# =====================================================
# DATABASE
# =====================================================
from app.data.db import connect_database
from app.data.incidents import (
    get_all_incidents,
    insert_incident,
)

DB_PATH = Path("DATA/intelligence_platform.db")
conn = connect_database(DB_PATH)

from streamlit.components.v1 import html


username = st.session_state.get("username", "Unknown_User")
role = st.session_state.get("role", "Unknown_Role")

html(
    f"""
    <div style="position: relative; text-align: center; height: 220px; margin-bottom: 30px;">
        <!-- Import Orbitron font -->
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&display=swap" rel="stylesheet">

        <!-- TSParticles sphere behind the title -->
        <div id="holoSphere" style="
            position: absolute;
            top: 35%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 350px;
            height: 350px;
            z-index: 1;
        "></div>

        <!-- Dashboard Title -->
        <h1 style="
            position: relative;
            z-index: 2;
            font-family: 'Orbitron', sans-serif;
            color: #ffffff;
            text-shadow: 0 0 5px #ff33ff, 0 0 10px #ff33ff, 0 0 20px #ff33ff, 0 0 30px #bb00ff;
            font-size: 40px;
            margin: 0;
            padding-top: 40px;
        ">
            🛡️ Cyber Incidents Dashboard
        </h1>

        <!-- Logged in info -->
        <p style="
            position: relative;
            z-index: 2;
            font-family: 'Orbitron', sans-serif;
            color: #e0e0e0;
            font-size: 16px;
            margin-top: 5px;
        ">
            Logged in as <strong>{username}</strong> ({role})
        </p>
    </div>

    <!-- TSParticles Script -->
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
# LOAD INCIDENT DATA
# =====================================================
data = get_all_incidents(conn)

# --- PARSE TIMESTAMP ONCE ---
if "timestamp" in data.columns:
    # convert to datetime WITHOUT changing timezone
    data["timestamp"] = pd.to_datetime(
        data["timestamp"], errors="coerce", format="%Y-%m-%d %H:%M:%S.%f"
    )


# =====================================================
# FILTER PANEL (NEW)
# =====================================================
with st.container():
    with st.expander("🔍 Filters", expanded=False):
        colA, colB, colC, colD = st.columns(4)

        with colA:
            sev_filter = st.multiselect(
                "Severity",
                sorted(data["severity"].dropna().unique().tolist()),
                default=None,
            )

        with colB:
            status_filter = st.multiselect(
                "Status",
                sorted(data["status"].dropna().unique().tolist()),
                default=None,
            )

        with colC:
            cat_filter = st.multiselect(
                "Category",
                sorted(data["category"].dropna().unique().tolist()),
                default=None,
            )

        with colD:
            date_filter = st.date_input("Date Range", [])

# APPLY FILTERS
filtered = data.copy()

if sev_filter:
    filtered = filtered[filtered["severity"].isin(sev_filter)]

if status_filter:
    filtered = filtered[filtered["status"].isin(status_filter)]

if cat_filter:
    filtered = filtered[filtered["category"].isin(cat_filter)]

if len(date_filter) == 2:
    start, end = date_filter
    filtered = filtered[
        (filtered["timestamp"] >= pd.to_datetime(start))
        & (filtered["timestamp"] <= pd.to_datetime(end))
    ]

# =====================================================
# DATA MANAGEMENT & AI ASSISTANT
# =====================================================
from app.components.data_manager import DataManager
from app.services.ai_assistant import ai_assistant

# Initialize data manager - get expected columns from actual data
if not data.empty:
    expected_columns = list(data.columns)
else:
    expected_columns = [
        "incident_id",
        "timestamp",
        "severity",
        "category",
        "status",
        "description",
        "inserted_at",  # Include inserted_at if it exists in the database
    ]


# Helper function to insert incident from row dict
def insert_incident_from_row(conn, **row_dict):
    """Insert incident from row dictionary."""
    from app.data.incidents import SecurityIncident

    incident = SecurityIncident(
        conn=conn,
        incident_id=row_dict.get("incident_id"),
        timestamp=row_dict.get("timestamp"),
        severity=row_dict.get("severity"),
        category=row_dict.get("category"),
        status=row_dict.get("status"),
        description=row_dict.get("description"),
    )
    return incident.save()


data_manager = DataManager(
    "cyber_incidents", expected_columns, conn=conn, insert_func=insert_incident_from_row
)

# Get all data sources
matching_data = data_manager.get_matching_data()
unmatching_data = data_manager.get_unmatching_data()
manual_data = data_manager.get_manual_data()

# IMPORTANT: Combine with FULL data (not filtered) first, so manual rows are included
# Then apply filters to the combined dataset
combined_data = data_manager.combine_with_original(data)

# Parse timestamps in combined data (for manual/matching data that might not be parsed)
if "timestamp" in combined_data.columns:
    combined_data["timestamp"] = pd.to_datetime(
        combined_data["timestamp"], errors="coerce", format="%Y-%m-%d %H:%M:%S.%f"
    )

# Apply filters to combined data (so charts include manual/uploaded data)
filtered_combined = combined_data.copy()

if sev_filter:
    filtered_combined = filtered_combined[
        filtered_combined["severity"].isin(sev_filter)
    ]

if status_filter:
    filtered_combined = filtered_combined[
        filtered_combined["status"].isin(status_filter)
    ]

if cat_filter:
    filtered_combined = filtered_combined[
        filtered_combined["category"].isin(cat_filter)
    ]

if len(date_filter) == 2:
    start, end = date_filter
    filtered_combined = filtered_combined[
        (filtered_combined["timestamp"] >= pd.to_datetime(start))
        & (filtered_combined["timestamp"] <= pd.to_datetime(end))
    ]

# Save the original filtered database data length for deletion logic
original_filtered_db_len = len(filtered)

# For display in data editor, use filtered_combined (filtered version of combined data)
# But keep the original filtered for backward compatibility if needed
filtered = filtered_combined.copy()

# =====================================================
# DATA DISPLAY
# =====================================================
st.markdown("### 📄 Data View")

# Database with tabs
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

        # Use data editor with delete capability - full width display
        edited_df = st.data_editor(
            display_data,
            use_container_width=True,
            height=500,
            num_rows="dynamic",
            key="combined_data_editor",
            disabled=["Row #"],  # Make row number non-editable
            hide_index=True,  # Hide default index
        )

        # Handle row deletions from data editor
        # Remove "Row #" column for processing
        if "Row #" in edited_df.columns:
            edited_df_clean = edited_df.drop(columns=["Row #"]).reset_index(drop=True)
        else:
            edited_df_clean = edited_df.reset_index(drop=True)

        # Check if rows were deleted by comparing lengths
        original_combined_len = len(filtered_combined)
        current_len = len(edited_df_clean)

        # Track processed deletions to prevent infinite rerun loop
        deletion_tracking_key = "cyber_deletion_tracking"
        deletion_processed_key = "cyber_deletion_processed"

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
            # Get list of incident_ids from database
            db_incident_ids = set(data["incident_id"].astype(str).unique())

            # Separate remaining rows into database vs manual/matching
            remaining_manual_matching = []
            for idx, row in edited_df_clean.iterrows():
                incident_id = str(row.get("incident_id", ""))
                # If incident_id is not in database, it's a manual/matching row
                if incident_id not in db_incident_ids:
                    remaining_manual_matching.append(row)

            # Convert to DataFrame
            if remaining_manual_matching:
                remaining_df = pd.DataFrame(remaining_manual_matching)
                # Try to preserve matching vs manual split if possible
                # But simpler: just put all remaining in manual (matching data is usually inserted into DB anyway)
                st.session_state["cyber_incidents_manual_data"] = (
                    remaining_df.reset_index(drop=True)
                )
                # Clear matching data (it's usually inserted into DB, so if it's still here, treat as manual)
                st.session_state["cyber_incidents_matching_data"] = pd.DataFrame()
            else:
                # All manual/matching rows deleted
                st.session_state["cyber_incidents_matching_data"] = pd.DataFrame()
                st.session_state["cyber_incidents_manual_data"] = pd.DataFrame()

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
            height=500,
            num_rows="dynamic",
            key="unmatching_data_editor",
            disabled=["Row #"],
            hide_index=True,
        )
        if st.button("🗑️ Clear All Unmatching Data", key="clear_unmatching"):
            st.session_state["cyber_incidents_unmatching_data"] = pd.DataFrame()
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
            key="manual_data_editor",
            disabled=["Row #"],
            hide_index=True,
        )
        if st.button("🗑️ Clear All Manual Data", key="clear_manual"):
            st.session_state["cyber_incidents_manual_data"] = pd.DataFrame()
            st.rerun()
    else:
        st.info("No manually added data")

# =====================================================
# CSV UPLOAD & MANUAL ENTRY SECTION
# =====================================================
st.markdown("---")
st.markdown("### 📤 Upload CSV or Add Data Manually")

# Create layout: CSV upload section
upload_col1 = st.container()

with upload_col1:
    st.markdown("#### 📁 Upload CSV File")
    uploaded_file = st.file_uploader(
        "Choose CSV file", type="csv", key="cyber_csv_upload"
    )

    # Continue with CSV processing...

    # Track processed files to prevent infinite rerun loop
    processed_files_key = "cyber_processed_files"
    if processed_files_key not in st.session_state:
        st.session_state[processed_files_key] = set()

    # Track if we're currently processing to prevent concurrent processing
    processing_key = "cyber_processing"
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
            if st.button("🔄 Clear processed files list", key="clear_processed_cyber"):
                st.session_state[processed_files_key] = set()
                st.rerun()
        elif st.session_state[processing_key]:
            # Currently processing, show loading message
            st.info("⏳ Processing file... Please wait.")
            # Add a button to reset stuck processing flag (safety mechanism)
            if st.button(
                "🔄 Reset Processing (if stuck)", key="reset_processing_cyber"
            ):
                st.session_state[processing_key] = False
                st.rerun()

# Create a new layout: Chatbox on left, Manual entry on right
upload_col2a, upload_col2b = st.columns(2)

with upload_col2a:
    # Draggable Chatbox (Simple AI - No API Required)
    from app.components.draggable_chatbox import draggable_chatbox

    # Get fresh unmatching data each time (in case new data was added)
    current_unmatching_data = data_manager.get_unmatching_data()

    draggable_chatbox(
        title="Simple AI Assistant",
        context_df=filtered_combined,
        role_hint="cyber_incident",
        unmatching_df=current_unmatching_data,
    )

with upload_col2b:
    st.markdown("#### ✏️ Add Row Manually")
    with st.form("manual_entry_form"):
        manual_col1, manual_col2 = st.columns(2)

        with manual_col1:
            manual_category = st.text_input("Category", key="manual_category")
            manual_severity = st.selectbox(
                "Severity", ["Low", "Medium", "High", "Critical"], key="manual_severity"
            )
            manual_status = st.selectbox(
                "Status", ["Open", "In Progress", "Resolved"], key="manual_status"
            )

        with manual_col2:
            # Auto-generate timestamp if not provided
            default_timestamp = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            manual_timestamp = st.text_input(
                "Timestamp",
                value=default_timestamp,
                key="manual_timestamp",
                help="Leave empty to use current time",
            )
            manual_incident_id = st.text_input(
                "Incident ID",
                value=f"INC{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}",
                key="manual_incident_id",
            )
            manual_description = st.text_area("Description", key="manual_description")

        if st.form_submit_button("Add Row"):
            # ALWAYS use current timestamp - ignore user input to guarantee it's never None
            final_timestamp = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")

            row_data = {
                "incident_id": (
                    manual_incident_id
                    if manual_incident_id
                    else f"INC{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}"
                ),
                "timestamp": final_timestamp,  # Always current time - never None
                "severity": manual_severity,
                "category": manual_category,
                "status": manual_status,
                "description": manual_description if manual_description else "",
            }

            # Debug: Show what we're passing
            # st.write(f"Debug - Timestamp being passed: {final_timestamp}")

            if data_manager.add_manual_row(row_data):
                st.success("Row added successfully!")
                st.rerun()


# =====================================================
# KPI CARDS (UPGRADED)
# =====================================================
st.markdown("## 📊 Analytics")

c1, c2, c3, c4 = st.columns(4)

c1.markdown(
    f"""
    <div style="padding: 0 9px;">
        <div class="metric-card">
            <h3>Total Incidents</h3>
            <div class="metric-value">{len(filtered_combined)}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

c2.markdown(
    f"""
    <div style="padding: 0 80px;">
        <div class="metric-card">
            <h3>High Severity</h3>
            <div class="metric-value">{(filtered_combined['severity']=='High').sum()}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

c3.markdown(
    f"""
    <div style="padding: 0 150px;">
        <div class="metric-card">
            <h3>Open Incidents</h3>
            <div class="metric-value">{(filtered_combined['status']=='Open').sum()}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

c4.markdown(
    f"""
    <div style="padding: 0 220px;">
        <div class="metric-card">
            <h3>Categories</h3>
            <div class="metric-value">{filtered_combined['category'].nunique()}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# ANALYTIC CHARTS (NEW LAYOUT)
# =====================================================

import plotly.express as px

# ------------------ PIE CHART: Severity Distribution ------------------
severity_colors = {
    "Low": "#00ffcc",
    "Medium": "#00ccff",
    "High": "#ff33ff",
    "Critical": "#ff0000",
}

fig1 = px.pie(
    filtered_combined,
    names="severity",
    title="🛡️ Severity Distribution",
    color="severity",
    color_discrete_map=severity_colors,
    hole=0.45,
)
fig1.update_traces(
    textinfo="percent+label",
    pull=[0.08] * len(filtered_combined["severity"].unique()),
    hoverinfo="label+percent+value",
    marker=dict(line=dict(color="#ffffff", width=2)),
)
fig1.update_layout(
    title_font=dict(family="Orbitron", size=28, color="#ff33ff"),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    legend_title_font=dict(family="Orbitron", color="#ffffff"),
    legend_font=dict(family="Orbitron", color="#ffffff"),
    margin=dict(t=60, b=20, l=20, r=20),
    height=550,
)

# ------------------ BAR CHART: Incidents by Category ------------------
cat_counts = filtered_combined.groupby("category").size().reset_index(name="count")
fig2 = px.bar(
    cat_counts,
    x="category",
    y="count",
    title="📊 Incidents by Category",
    color="count",
    color_continuous_scale=["#bb00ff", "#ff33ff"],
    text="count",
)
fig2.update_traces(
    marker_line_color="#ffffff",
    marker_line_width=2,
    hovertemplate="<b>%{x}</b><br>Incidents: %{y}<extra></extra>",
)
fig2.update_layout(
    title_font=dict(family="Orbitron", size=28, color="#ff33ff"),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis_title=None,
    yaxis_title="Count",
    font=dict(family="Orbitron", color="#ffffff"),
    coloraxis_showscale=False,
    margin=dict(t=60, b=50, l=40, r=40),
    height=550,
)

# ------------------ LINE CHART: Trend Over Time ------------------
if "timestamp" in filtered_combined.columns:
    time_series = (
        filtered_combined.dropna(subset=["timestamp"])
        .groupby(filtered_combined["timestamp"].dt.date)
        .size()
        .reset_index(name="count")
    )
    fig3 = px.line(
        time_series,
        x="timestamp",
        y="count",
        title="📈 Trend Over Time",
        markers=True,
    )
    fig3.update_traces(
        line_color="#ff33ff",
        line_width=4,
        marker=dict(size=12, color="#00ffcc", line=dict(width=2, color="#ffffff")),
        hovertemplate="<b>%{x}</b><br>Incidents: %{y}<extra></extra>",
    )
    fig3.update_layout(
        title_font=dict(family="Orbitron", size=28, color="#ff33ff"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)"),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)"),
        font=dict(family="Orbitron", color="#ffffff"),
        margin=dict(t=60, b=50, l=40, r=40),
        height=550,
    )

# ------------------ HEATMAP: Severity vs Category ------------------
fig4 = px.density_heatmap(
    filtered_combined,
    x="category",
    y="severity",
    title="🔥 Severity vs Category Heatmap",
    color_continuous_scale=["#00ffcc", "#bb00ff", "#ff33ff", "#ff0000"],
)
fig4.update_traces(
    hovertemplate="<b>%{y}</b> in <b>%{x}</b><br>Count: %{z}<extra></extra>"
)
fig4.update_layout(
    title_font=dict(family="Orbitron", size=28, color="#ff33ff"),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False),
    font=dict(family="Orbitron", color="#ffffff"),
    margin=dict(t=60, b=50, l=40, r=40),
    height=550,
)

# ------------------ RENDER CHARTS STACKED FULL-WIDTH ------------------
for fig in [fig1, fig2, fig3, fig4]:
    st.plotly_chart(
        fig,
        config={"displayModeBar": False},  # hide toolbar
        theme="streamlit",
        use_container_width=True,
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
        title="Cyber Incidents AI Assistant",
        context_df=filtered_combined,
        role_hint="cyber_incident",
        primary_key_name="incident_id",
    )
except Exception as e:
    st.error(f"⚠️ Premium AI unavailable: {str(e)[:100]}")
    st.info("💡 Try using the Simple AI Assistant above!")
