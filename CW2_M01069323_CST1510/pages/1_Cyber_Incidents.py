import streamlit as st
import pandas as pd
from pathlib import Path
from app.components.sidebar import render_sidebar
render_sidebar()



# =====================================================
# ACCESS CONTROL + REDIRECT TO LOGIN
# =====================================================

# SAFE DEFAULT SESSION VALUES
st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("username", None)
st.session_state.setdefault("role", None)

# LOGIN REQUIRED
if not st.session_state.logged_in:
    st.switch_page("pages/0_Login.py")

# ROLE CHECK
role = (st.session_state.role or "").strip().lower()
if role != "cyber":
    st.error("You do not have permission to access the Cyber Dashboard!")
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
from app.data.incidents import (
    get_all_incidents,
    insert_incident,
    get_incidents_by_type_count,
    get_high_severity_by_status,
)

DB_PATH = Path("DATA/intelligence_platform.db")
conn = connect_database(DB_PATH)

# =====================================================
# PAGE CONTENT
# =====================================================
st.title(" Cyber Incidents Dashboard")
st.write(f"Logged in as **{st.session_state.username}** ({role})")

# READ
st.subheader(" All Incidents")
data = get_all_incidents(conn)
st.dataframe(data, width="stretch")


# CREATE INCIDENT
# CREATE INCIDENT
st.subheader(" Add New Incident")
with st.form("incident_form"):
    col1, col2 = st.columns(2)

    with col1:
        date = st.date_input("Incident Date")
        incident_type = st.text_input("Incident Type")
        severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])

    with col2:
        status = st.selectbox("Status", ["Open", "In Progress", "Resolved"])
        reported_by = st.text_input("Reported By", st.session_state.username)

    description = st.text_area("Description")
    submitted = st.form_submit_button("Create Incident")

if submitted:
    new_id = insert_incident(
        conn,
        category=incident_type,   # category = incident_type input
        severity=severity,
        status=status,
        description=description
)

    st.success(f"Incident created successfully! ID = {new_id}")
    st.rerun()


# ANALYTICS
st.subheader(" Analytics")
tab1, tab2 = st.tabs(["By Type", "High Severity"])

with tab1:
    df = get_incidents_by_type_count(conn)

# Ensure df is a proper DataFrame
    df = pd.DataFrame(df)

    if not df.empty and "category" in df.columns:
        st.bar_chart(df.set_index("category"), use_container_width=True)

    else:
        st.info("No data available.")

with tab2:
    df = get_high_severity_by_status(conn)
    df = pd.DataFrame(df)

    if not df.empty and "status" in df.columns:
        st.bar_chart(df.set_index("status"), use_container_width=True)
    else:
         st.info("No critical incidents found.")


# AI ASSISTANT
from app.services.ai_assistant import ai_assistant

st.markdown("---")

with st.container():
    ai_assistant(
        "Cybersecurity AI Assistant",
        context_df=data   # the incident table here
    )

