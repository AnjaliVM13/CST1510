import streamlit as st
import pandas as pd
from pathlib import Path
from app.components.sidebar import render_sidebar
render_sidebar()



# =====================================================
# ACCESS CONTROL + REDIRECT TO LOGIN
# =====================================================
st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("username", None)
st.session_state.setdefault("role", None)

if not st.session_state.logged_in:
    st.switch_page("pages/0_Login.py")

role = (st.session_state.role or "").strip().lower()
if role != "data":
    st.error("You do not have permission to access the Data Dashboard!")
    st.stop()



# =====================================================
# DARK MODE STYLING
# =====================================================
st.markdown("""
<style>
body { background-color: #0E1117; }
.block-container { background-color: #0E1117; padding-top: 20px; }
h1, h2, h3, h4 { color: white !important; }
.dataframe { background-color: #1E1E1E; color: white; }
.stButton>button {
    background-color: #4F46E5;
    color: white;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

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

# =====================================================
# PAGE CONTENT
# =====================================================
st.title("Dataset Management Dashboard")
st.write(f"Logged in as **{st.session_state.username}** ({role})")

# -----------------------------------------------------
# VIEW DATASETS
# -----------------------------------------------------
st.subheader("Stored Datasets")

df = get_all_datasets(conn)
if df.empty:
    st.info("No datasets stored yet.")
else:
    st.dataframe(df, use_container_width=True)


# -----------------------------------------------------
# UPLOAD NEW DATASET
# -----------------------------------------------------
st.subheader("Upload New Dataset")

uploaded_file = st.file_uploader("Upload CSV file", type="csv")
dataset_name = st.text_input("Dataset Name (required)")
uploaded_by = st.text_input("Uploaded By", st.session_state.username)

if uploaded_file and dataset_name.strip():
    df_csv = pd.read_csv(uploaded_file)

    st.write("### Preview")
    st.dataframe(df_csv.head(), use_container_width=True)

    if st.button("Save Dataset Metadata"):
        new_id = insert_dataset_metadata(
            conn,
            name=dataset_name,
            rows=len(df_csv),
            columns=len(df_csv.columns),
            uploaded_by=uploaded_by,
            upload_date=str(pd.Timestamp.now().date())
        )
        st.success(f"Dataset metadata saved! ID = {new_id}")
        st.rerun()

# -----------------------------------------------------
# AI ASSISTANT
# -----------------------------------------------------
from app.services.ai_assistant import ai_assistant

st.markdown("---")
ai_assistant(
    title="Data Science AI Assistant",
    context_df=df
)

