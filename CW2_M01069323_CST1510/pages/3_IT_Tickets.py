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
if role != "it":
    st.error("You do not have permission to access the IT Dashboard!")
    st.stop()



# =====================================================
# DARK MODE THEME
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
# DATABASE
# =====================================================
from app.data.db import connect_database
from app.data.tickets import (
    insert_ticket,
    get_all_tickets,
    update_ticket_status,
    get_ticket_priority_counts,
)

DB_PATH = Path("DATA/intelligence_platform.db")
conn = connect_database(DB_PATH)

# =====================================================
# PAGE CONTENT
# =====================================================
st.title("🛠 IT Tickets Dashboard")
st.write(f"Logged in as **{st.session_state.username}** ({role})")

# -----------------------------------------------------
# VIEW TICKETS
# -----------------------------------------------------
st.subheader("All Tickets")
df = get_all_tickets(conn)

if df.empty:
    st.info("No tickets yet.")
else:
    st.dataframe(df, use_container_width="stretch")

# -----------------------------------------------------
# CREATE NEW TICKET
# -----------------------------------------------------
st.subheader("Create New Ticket")

with st.form("ticket_form"):
    col1, col2 = st.columns(2)

    with col1:
        priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
        description = st.text_area("Description")

    with col2:
        status = st.selectbox("Status", ["Open", "In Progress", "Resolved"])
        assigned_to = st.text_input("Assigned To", st.session_state.username)

    submitted = st.form_submit_button("Submit Ticket")

if submitted:
    new_id = insert_ticket(conn, priority, description, status, assigned_to, 0)
    st.success(f"Ticket created successfully! ID = {new_id}")
    st.rerun()

# -----------------------------------------------------
# ANALYTICS
# -----------------------------------------------------
st.subheader("Ticket Priority Distribution")

df_pri = get_ticket_priority_counts(conn)
if not df_pri.empty:
    st.bar_chart(df_pri.set_index("priority"))
else:
    st.info("No data for chart.")

# -----------------------------------------------------
# AI ASSISTANT
# -----------------------------------------------------
from app.services.ai_assistant import ai_assistant

st.markdown("---")
ai_assistant(
    title="IT Support AI Assistant",
    context_df=df     # <AI can see the IT tickets table!
)


