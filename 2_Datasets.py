import streamlit as st
import plotly.express as px
import pandas as pd
import sys
from pathlib import Path

# Make sure Python can find the 'app' folder BEFORE importing from it
sys.path.append(str(Path(__file__).resolve().parent.parent))
from app.components.sidebar import render_sidebar
from app.theme.dashboard_effects import apply_dashboard_effects

apply_dashboard_effects()

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
# SIDEBAR
# =====================================================
from app.components.sidebar import render_sidebar

render_sidebar()
# =====================================================
# ACCESS CONTROL + REDIRECT TO LOGIN
# =====================================================
st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("username", None)
st.session_state.setdefault("role", None)

if not st.session_state.logged_in:
    st.switch_page("pages/Close.py")

role = (st.session_state.role or "").strip().lower()
if role != "data":
    st.error("You do not have permission to access the Data Dashboard!")
    st.stop()


# =====================================================
# CUSTOM "GAMING" FONTS + CARD STYLING
# =====================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&display=swap');

    /* Titles with neon glow */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5 {
        font-family: 'Orbitron', sans-serif;
        color: #ffffff;
        text-shadow: 0 0 5px #ff33ff, 0 0 10px #ff33ff, 0 0 20px #ff33ff, 0 0 30px #bb00ff;
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
        margin-right: 15px;   /* horizontal spacing between cards */
        margin-bottom: 20px;  /* vertical spacing */
        display: inline-block;
    }
    .metric-card:hover {
        box-shadow: 0 0 25px rgba(255,0,255,0.8);
        transform: scale(1.05);
    }

    /* Metric value style */
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #A78BFA;
    }

    /* Buttons */
    .stButton>button {
        font-family: 'Orbitron', sans-serif;
        font-weight: bold;
        color: #ffffff;
        text-shadow: 0 0 3px #ff00ff;
        border-radius: 12px;
        padding: 10px 14px;
        font-size: 16px;
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
# PAGE HEADER + HOLOGRAPHIC PARTICLES
# =====================================================
from streamlit.components.v1 import html

username = st.session_state.username

html(
    f"""
    <div style="position: relative; text-align: center; height: 220px; margin-bottom: 30px;">
        <!-- Import Orbitron font -->
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&display=swap" rel="stylesheet">   
        <div id="holoSphere" style="
            position: absolute;
            top: 50%;
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
            💾 Dataset Dashboard
        </h1>

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

    <script src="https://cdn.jsdelivr.net/npm/tsparticles@2.11.1/tsparticles.bundle.min.js"></script>
    <script>
    tsParticles.load("holoSphere", {{
        fullScreen: false,
        background: {{ color: "transparent" }},
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
# DATABASE CONNECTION
# =====================================================
from app.data.db import connect_database
from app.data.datasets import (
    insert_dataset_metadata,
    get_all_datasets,
)

DB_PATH = Path("DATA/intelligence_platform.db")
conn = connect_database(DB_PATH)


# fetch
df = get_all_datasets(conn)

# ensure upload_date is datetime if you need date sorting/filtering
if "upload_date" in df.columns:
    df["upload_date"] = pd.to_datetime(df["upload_date"], errors="coerce")

# sort by dataset_id ascending and reset index so left column becomes 0..n-1
df = df.sort_values(by="dataset_id", ascending=True).reset_index(drop=True)


# =====================================================
# FILTER PANEL FOR DATASETS
# =====================================================
st.subheader("Filter Datasets")

with st.container():
    with st.expander("🔍 Filters", expanded=False):
        colA, colB, colC, colD = st.columns(4)

        # Dataset Type
with colA:
    name_filter = st.multiselect(
        "Dataset Name", sorted(df["name"].dropna().unique().tolist()), default=None
    )

with colB:
    uploaded_by_filter = st.multiselect(
        "Uploaded By",
        sorted(df["uploaded_by"].dropna().unique().tolist()),
        default=None,
    )

with colC:
    # Optional: status filter if you have a status column
    pass

with colD:
    date_filter = st.date_input("Created Date Range", [])


# =====================================================
# APPLY FILTERS
# =====================================================
filtered_df = df.copy()

# Apply filters using existing columns
if name_filter:
    filtered_df = filtered_df[filtered_df["name"].isin(name_filter)]

if uploaded_by_filter:
    filtered_df = filtered_df[filtered_df["uploaded_by"].isin(uploaded_by_filter)]

# Date range filter
if len(date_filter) == 2:
    start, end = date_filter
    filtered_df = filtered_df[
        (filtered_df["upload_date"] >= pd.to_datetime(start))
        & (filtered_df["upload_date"] <= pd.to_datetime(end))
    ]

# Ensure upload_date is datetime
filtered_df["upload_date"] = pd.to_datetime(filtered_df["upload_date"])

# Date range filter
if len(date_filter) == 2:
    start, end = date_filter
    filtered_df = filtered_df[
        (filtered_df["upload_date"] >= pd.to_datetime(start))
        & (filtered_df["upload_date"] <= pd.to_datetime(end))
    ]

# Save original unfiltered data before overwriting df
original_df = df.copy()

# Overwrite df with filtered_df for backward compatibility
df = filtered_df

# =====================================================
# DATA MANAGEMENT & AI ASSISTANT
# =====================================================
from app.components.data_manager import DataManager
from app.services.ai_assistant import ai_assistant

# Initialize data manager - get expected columns from actual data
if not original_df.empty:
    expected_columns = list(original_df.columns)
else:
    expected_columns = [
        "dataset_id",
        "name",
        "rows",
        "columns",
        "uploaded_by",
        "upload_date",
    ]


# Helper function to insert dataset from row dict
def insert_dataset_from_row(conn, **row_dict):
    """Insert dataset from row dictionary."""
    from app.data.datasets import Dataset

    dataset = Dataset(
        conn=conn,
        dataset_id=row_dict.get("dataset_id"),
        name=row_dict.get("name"),
        rows=row_dict.get("rows"),
        columns=row_dict.get("columns"),
        uploaded_by=row_dict.get("uploaded_by"),
        upload_date=row_dict.get("upload_date"),
    )
    return dataset.save()


data_manager = DataManager(
    "datasets", expected_columns, conn=conn, insert_func=insert_dataset_from_row
)

# Get all data sources
matching_data = data_manager.get_matching_data()
unmatching_data = data_manager.get_unmatching_data()
manual_data = data_manager.get_manual_data()

# IMPORTANT: Combine with FULL original data (not filtered) first, so manual rows are included
# Then apply filters to the combined dataset
combined_data = data_manager.combine_with_original(original_df)

# Parse upload_date in combined data (for manual/matching data that might not be parsed)
if "upload_date" in combined_data.columns:
    combined_data["upload_date"] = pd.to_datetime(
        combined_data["upload_date"], errors="coerce"
    )

# Apply filters to combined data (so charts include manual/uploaded data)
filtered_combined = combined_data.copy()

if name_filter:
    filtered_combined = filtered_combined[filtered_combined["name"].isin(name_filter)]

if uploaded_by_filter:
    filtered_combined = filtered_combined[
        filtered_combined["uploaded_by"].isin(uploaded_by_filter)
    ]

if len(date_filter) == 2:
    start, end = date_filter
    filtered_combined = filtered_combined[
        (filtered_combined["upload_date"] >= pd.to_datetime(start))
        & (filtered_combined["upload_date"] <= pd.to_datetime(end))
    ]

# Save the original filtered database data length for deletion logic
original_filtered_db_len = len(df)

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
            key="datasets_combined_editor",
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
        deletion_tracking_key = "datasets_deletion_tracking"
        deletion_processed_key = "datasets_deletion_processed"

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
            # Get list of dataset_ids from database
            db_dataset_ids = set(original_df["dataset_id"].astype(str).unique())

            # Separate remaining rows into database vs manual/matching
            remaining_manual_matching = []
            for idx, row in edited_df_clean.iterrows():
                dataset_id = str(row.get("dataset_id", ""))
                # If dataset_id is not in database, it's a manual/matching row
                if dataset_id not in db_dataset_ids:
                    remaining_manual_matching.append(row)

            # Convert to DataFrame
            if remaining_manual_matching:
                remaining_df = pd.DataFrame(remaining_manual_matching)
                # Put all remaining in manual (matching data is usually inserted into DB anyway)
                st.session_state["datasets_manual_data"] = remaining_df.reset_index(
                    drop=True
                )
                # Clear matching data
                st.session_state["datasets_matching_data"] = pd.DataFrame()
            else:
                # All manual/matching rows deleted
                st.session_state["datasets_matching_data"] = pd.DataFrame()
                st.session_state["datasets_manual_data"] = pd.DataFrame()

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
            key="datasets_unmatching_editor",
            disabled=["Row #"],
            hide_index=True,
        )
        if st.button("🗑️ Clear All Unmatching Data", key="clear_datasets_unmatching"):
            st.session_state["datasets_unmatching_data"] = pd.DataFrame()
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
            key="datasets_manual_editor",
            disabled=["Row #"],
            hide_index=True,
        )
        if st.button("🗑️ Clear All Manual Data", key="clear_datasets_manual"):
            st.session_state["datasets_manual_data"] = pd.DataFrame()
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
        "Choose CSV file", type="csv", key="datasets_csv_upload"
    )

    # Track processed files to prevent infinite rerun loop
    processed_files_key = "datasets_processed_files"
    if processed_files_key not in st.session_state:
        st.session_state[processed_files_key] = set()

    # Track if we're currently processing to prevent concurrent processing
    processing_key = "datasets_processing"
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
            if st.button(
                "🔄 Clear processed files list", key="clear_processed_datasets"
            ):
                st.session_state[processed_files_key] = set()
                st.rerun()
        elif st.session_state[processing_key]:
            # Currently processing, show loading message
            st.info("⏳ Processing file... Please wait.")
            # Add a button to reset stuck processing flag (safety mechanism)
            if st.button(
                "🔄 Reset Processing (if stuck)", key="reset_processing_datasets"
            ):
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
        role_hint="dataset",
        unmatching_df=current_unmatching_data,
    )

with upload_col2b:
    st.markdown("#### ✏️ Add Row Manually")
    with st.form("datasets_manual_form"):
        manual_dataset_id = st.text_input(
            "Dataset ID (optional - auto-generated if empty)"
        )
        manual_name = st.text_input("Dataset Name")
        manual_rows = st.number_input("Rows", min_value=0, value=0, step=1)
        manual_columns = st.number_input("Columns", min_value=0, value=0, step=1)
        manual_uploaded_by = st.text_input("Uploaded By", st.session_state.username)

        if st.form_submit_button("Add Row"):
            # ALWAYS use current timestamp
            final_timestamp = pd.Timestamp.now().strftime("%Y-%m-%d")
            row_data = {
                "dataset_id": (
                    manual_dataset_id
                    if manual_dataset_id
                    else f"DS{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}"
                ),
                "name": manual_name if manual_name else "",
                "rows": manual_rows,
                "columns": manual_columns,
                "uploaded_by": manual_uploaded_by,
                "upload_date": final_timestamp,  # Always current time - never None
            }
            if data_manager.add_manual_row(row_data):
                st.success("Row added successfully!")
                st.rerun()

# ===========================================================
# KPI METRICS (Using st.columns for proper horizontal layout)
# ===========================================================
st.markdown("## 📊 Dataset Analytics")

c1, c2, c3 = st.columns(3, gap="large")

with c1:
    st.markdown(
        f"""
    <div style="padding: 0 10px;">
        <div class="metric-card">
            <h3>Total Datasets</h3>
            <div class="metric-value">{len(filtered_combined)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        f"""
        <div style="padding: 0 10px;">
        <div class="metric-card">
            <h3>Avg Rows</h3>
            <div class="metric-value">{int(filtered_combined['rows'].mean()) if not filtered_combined.empty else 0}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        f"""
        <div style="padding: 0 10px;">
        <div class="metric-card">
            <h3>Avg Columns</h3>
            <div class="metric-value">{int(filtered_combined['columns'].mean()) if not filtered_combined.empty else 0}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd


# ---------- Function to apply neon-dark theme ----------
def apply_neon_dark_theme(fig):
    fig.update_layout(
        font_family="Orbitron",
        font_color="#ffffff",
        plot_bgcolor="#0a0a0f",
        paper_bgcolor="#0a0a0f",
        title_font=dict(color="#bb00ff", size=22),
        legend_font=dict(color="#bb00ff"),
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(187,0,255,0.2)",
            linecolor="#bb00ff",
            linewidth=2,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(187,0,255,0.2)",
            linecolor="#bb00ff",
            linewidth=2,
        ),
    )
    return fig


import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ---------- Datasets Uploaded By ----------
st.markdown("## 📈 Datasets Uploaded By")

fig_bar = px.bar(
    filtered_combined.groupby("uploaded_by").size().reset_index(name="count"),
    x="uploaded_by",
    y="count",
    text="count",
    title="Datasets Uploaded By",
)
fig_bar.update_traces(
    marker=dict(color="rgba(187,0,255,0.6)", line=dict(color="#bb00ff", width=3)),
    textposition="outside",
)
fig_bar.update_layout(
    width=1200,
    height=700,
    title_font=dict(family="Orbitron", color="#bb00ff", size=28),
    xaxis_title_font=dict(family="Orbitron", color="#bb00ff", size=18),
    yaxis_title_font=dict(family="Orbitron", color="#bb00ff", size=18),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
)
apply_neon_dark_theme(fig_bar)
st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": True})

# ---------- Pie Chart ----------
st.markdown("## 🥧 Uploaded By Distribution")

pie_column = "uploaded_by"
counts = filtered_combined[pie_column].value_counts().reset_index()
counts.columns = [pie_column, "count"]
fig_pie = px.pie(
    counts,
    names=pie_column,
    values="count",
    hole=0.4,
    color_discrete_sequence=["#bb00ff", "#ff33ff", "#a78bfa", "#7C3AED", "#D8B4FE"],
    title=f"{pie_column} Distribution",
)
fig_pie.update_traces(
    textinfo="label+percent",
    textfont=dict(family="Orbitron", color="#ffffff", size=18),
    marker=dict(line=dict(color="#bb00ff", width=3)),
)
fig_pie.update_layout(
    width=1200, height=700, title_font=dict(family="Orbitron", color="#bb00ff", size=28)
)
apply_neon_dark_theme(fig_pie)
st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": True})

# ---------- Row Count Distribution ----------
st.markdown("## 📊 Row Count Distribution")
fig_rows = px.histogram(
    filtered_combined, x="rows", nbins=20, title="Row Count Distribution"
)
fig_rows.update_traces(
    marker=dict(color="rgba(187,0,255,0.6)", line=dict(color="#bb00ff", width=3))
)
fig_rows.update_layout(width=1200, height=700)
apply_neon_dark_theme(fig_rows)
st.plotly_chart(fig_rows, use_container_width=True, config={"displayModeBar": True})

# ---------- Column Count Distribution ----------
st.markdown("## 📊 Column Count Distribution")
fig_cols = px.histogram(
    filtered_combined, x="columns", nbins=15, title="Column Count Distribution"
)
fig_cols.update_traces(
    marker=dict(color="rgba(187,0,255,0.6)", line=dict(color="#bb00ff", width=3))
)
fig_cols.update_layout(width=1200, height=700)
apply_neon_dark_theme(fig_cols)
st.plotly_chart(fig_cols, use_container_width=True, config={"displayModeBar": True})

# ---------- Animated Line Chart ----------
st.markdown("## 📈 Dataset Growth Over Time")
df_time = (
    filtered_combined.groupby(filtered_combined["upload_date"].dt.date)
    .size()
    .reset_index(name="count")
)
frames = []
widths = np.linspace(3, 7, 10)
for w in widths:
    frames.append(
        go.Frame(
            data=[
                go.Scatter(
                    x=df_time["upload_date"],
                    y=df_time["count"],
                    mode="lines+markers",
                    line=dict(color="#bb00ff", width=w, shape="spline", smoothing=1.3),
                    marker=dict(
                        size=12, color="#a78bfa", line=dict(color="#bb00ff", width=2)
                    ),
                )
            ],
            name=str(w),
        )
    )

fig_line = go.Figure(
    data=[
        go.Scatter(
            x=df_time["upload_date"],
            y=df_time["count"],
            mode="lines+markers",
            line=dict(color="#bb00ff", width=4, shape="spline", smoothing=1.3),
            marker=dict(size=12, color="#a78bfa", line=dict(color="#bb00ff", width=2)),
        )
    ],
    frames=frames,
)
fig_line.update_layout(
    width=1200,
    height=700,
    updatemenus=[
        dict(
            type="buttons",
            showactive=False,
            buttons=[
                dict(
                    label="Play",
                    method="animate",
                    args=[
                        None,
                        dict(
                            frame=dict(duration=300, redraw=True),
                            fromcurrent=True,
                            mode="loop",
                        ),
                    ],
                )
            ],
        )
    ],
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
)
apply_neon_dark_theme(fig_line)
st.plotly_chart(fig_line, use_container_width=True, config={"displayModeBar": True})

# ---------- Scatter Plot ----------
st.markdown("## 🔬 Rows vs Columns Scatter")
fig_scatter = px.scatter(
    filtered_combined,
    x="columns",
    y="rows",
    color="rows",
    size="rows",
    hover_data=["name"],
    title="Rows vs Columns",
)
fig_scatter.update_traces(
    marker=dict(color="rgba(187,0,255,0.7)", line=dict(color="#bb00ff", width=2))
)
fig_scatter.update_layout(width=1200, height=700)
apply_neon_dark_theme(fig_scatter)
st.plotly_chart(fig_scatter, use_container_width=True, config={"displayModeBar": True})

# ---------- Enhanced Heatmap ----------
st.markdown("## 🔥 Rows vs Columns Heatmap")
if not filtered_combined.empty:
    heatmap_data = (
        filtered_combined.groupby(["rows", "columns"]).size().reset_index(name="count")
    )
    fig_heat = go.Figure(
        data=go.Heatmap(
            x=heatmap_data["columns"],
            y=heatmap_data["rows"],
            z=heatmap_data["count"],
            colorscale=[
                [0, "#00ffcc"],
                [0.33, "#bb00ff"],
                [0.66, "#ff33ff"],
                [1, "#ff0000"],
            ],
            showscale=True,
            colorbar=dict(
                title=dict(
                    text="Count", font=dict(family="Orbitron", color="#ffffff", size=14)
                ),
                tickfont=dict(family="Orbitron", color="#ffffff", size=12),
            ),
            hovertemplate="<b>Rows:</b> %{y}<br><b>Columns:</b> %{x}<br><b>Count:</b> %{z}<extra></extra>",
        )
    )
    fig_heat.update_layout(
        title=dict(
            text="🔥 Rows vs Columns Heatmap",
            font=dict(family="Orbitron", size=32, color="#bb00ff"),
            x=0.5,
            xanchor="center",
        ),
        xaxis=dict(
            title=dict(
                text="Columns", font=dict(family="Orbitron", color="#bb00ff", size=18)
            ),
            tickfont=dict(family="Orbitron", color="#ffffff", size=12),
            linecolor="#bb00ff",
            linewidth=2,
        ),
        yaxis=dict(
            title=dict(
                text="Rows", font=dict(family="Orbitron", color="#bb00ff", size=18)
            ),
            tickfont=dict(family="Orbitron", color="#ffffff", size=12),
            linecolor="#bb00ff",
            linewidth=2,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=80, b=50, l=40, r=40),
        height=600,
    )
    st.plotly_chart(
        fig_heat, use_container_width=True, config={"displayModeBar": False}
    )
else:
    st.info("No data available for heatmap")

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
        title="Datasets AI Assistant",
        context_df=filtered_combined,  # Use filtered combined data
        role_hint="dataset",
        primary_key_name="dataset_id",
    )
except Exception as e:
    st.error(f"⚠️ Premium AI unavailable: {str(e)[:100]}")
    st.info("💡 Try using the Simple AI Assistant above!")
