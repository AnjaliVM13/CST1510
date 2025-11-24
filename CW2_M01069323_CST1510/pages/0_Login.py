import streamlit as st
from pathlib import Path

from app.data.db import connect_database
from app.services.user_service import register_user, login_user
from app.components.sidebar import render_sidebar
render_sidebar()
# -----------------------------
# PAGE / THEME SETTINGS
# -----------------------------
st.set_page_config(
    page_title="Login Portal",
    layout="centered",
)

st.markdown("""
<style>
/* Hide the entire toolbar (profile, settings, help) */
header[data-testid="stHeader"] { 
    display: none !important;
}

/* Hide top-right hamburger menu */
button[kind="header"] {
    display: none !important;
}

/* Hide menu overlay if it loads */
[data-testid="stToolbar"] {
    display: none !important;
}

/* Hide main menu (•••) fully */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# -----------------------------
# CONNECT TO DATABASE
# -----------------------------
DB_PATH = Path("DATA/intelligence_platform.db")
conn = connect_database(DB_PATH)

# -----------------------------
# SESSION STATE (important)
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = None

if "role" not in st.session_state:
    st.session_state.role = None

# -----------------------------
# CUSTOM CSS - DARK MODE UI
# -----------------------------
st.markdown("""
<style>
body { background-color: #0E1117 !important; }
.block-container { padding-top: 2rem; }

.login-box {
    background-color: #1E1E1E;
    padding: 35px;
    border-radius: 12px;
    width: 420px;
    margin: auto;
    box-shadow: 0px 0px 20px #00000055;
}
.login-title {
    text-align: center; 
    font-size: 28px; 
    color: white;
    margin-bottom: 10px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOGO + TITLE
# -----------------------------
st.image("assets/logo.png", width=180)
st.markdown("<h2 class='login-title'>Intelligence Platform Login</h2>", unsafe_allow_html=True)

# -----------------------------
# LOGIN + REGISTER TABS
# -----------------------------
tabs = st.tabs([" Login", " Register"])

# ======================================
#             LOGIN TAB
# ======================================
with tabs[0]:
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)

    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", type="password", placeholder="Enter your password")

    if st.button("Login", use_container_width=True):
        success, role = login_user(conn, username, password)


        if success:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = role

            st.success(f"Welcome back, {username}! Redirecting...")

            # REDIRECT BASED ON ROLE
            if role == "cyber":
                st.switch_page("pages/1_Cyber_Incidents.py")



            elif role == "data":
                st.switch_page("pages/2_Datasets.py")


            elif role == "it":
                st.switch_page("pages/3_IT_Tickets.py")


        else:
            st.error(role)

    st.markdown("</div>", unsafe_allow_html=True)

# ======================================
#           REGISTER TAB
# ======================================
with tabs[1]:
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)

    reg_user = st.text_input("Choose Username")
    reg_pass = st.text_input("Choose Password", type="password")
    reg_role = st.selectbox("Select Your Role", ["cyber", "data", "it"])

    if st.button("Register", use_container_width=True):
        success, msg = register_user(conn, reg_user, reg_pass, reg_role)

        if success:
            st.success("Account successfully created. You can now log in.")
        else:
            st.error(msg)

    st.markdown("</div>", unsafe_allow_html=True)
