import streamlit as st
from pathlib import Path
from app.components.sidebar import render_sidebar
render_sidebar()
# -------------------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------------------
st.set_page_config(page_title="Home Dashboard", layout="wide")

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

# -------------------------------------------------------------------
# AUTH CHECK
# -------------------------------------------------------------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("pages/0_Login.py")

username = st.session_state.username
role = st.session_state.role.lower().strip()

# -------------------------------------------------------------------
# ADVANCED SIDEBAR (Glass, Gradient Ring, Animated Links)
# -------------------------------------------------------------------
sidebar_css = """
<style>

    /* Sidebar Background Blur */
    section[data-testid="stSidebar"] {
        background: rgba(255,255,255,0.04);
        backdrop-filter: blur(14px);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    /* Profile Container */
    .profile-box {
        padding: 20px 15px;
        text-align: center;
    }

    /* Gradient Avatar Ring */
    .avatar-ring {
        width: 110px;
        height: 110px;
        margin: auto;
        border-radius: 50%;
        padding: 4px;
        background: linear-gradient(135deg, #6a5acd, #00c6ff, #7b61ff);
    }
    .avatar-pic {
        width: 102px;
        height: 102px;
        border-radius: 50%;
        background: #0e1117;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 42px;
        color: white;
        font-weight: 600;
    }

    /* Username */
    .profile-name {
        margin-top: 10px;
        color: white;
        font-size: 20px;
        font-weight: 600;
    }

    /* Role Badge */
    .role-badge {
        display: inline-block;
        margin-top: 4px;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
        color: white;
    }

    .role-cyber   { background: #ff4f4f55; }
    .role-data    { background: #4fc3f755; }
    .role-it      { background: #7bff5e55; }

    /* Sidebar Links Animation */
    .nav-link {
        padding: 10px 14px;
        margin: 6px 0;
        border-radius: 8px;
        color: white !important;
        font-size: 15px;
        transition: 0.18s ease;
    }
    .nav-link:hover {
        background: rgba(255,255,255,0.08);
        padding-left: 18px;
    }

    /* Logout Floating Button */
    .logout-btn {
        width: 100%;
        padding: 10px;
        margin-top: 10px;
        border-radius: 8px;
        background: #ff4b4b;
        color: white !important;
        text-align: center;
        font-weight: 600;
        transition: 0.2s;
    }
    .logout-btn:hover {
        background: #ff2e2e;
        transform: scale(1.02);
    }

</style>
"""

st.markdown(sidebar_css, unsafe_allow_html=True)

# -------------------------------------------------------------------
# SIDEBAR CONTENT
# -------------------------------------------------------------------
with st.sidebar:
    st.markdown("<div class='profile-box'>", unsafe_allow_html=True)

    # Avatar ring with first letter of name
    st.markdown(
        f"""
        <div class="avatar-ring">
            <div class="avatar-pic">{username[0].upper()}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Username
    st.markdown(f"<div class='profile-name'>{username}</div>", unsafe_allow_html=True)

    # Role Badge
    st.markdown(
        f"<div class='role-badge role-{role}'>{role.upper()}</div>",
        unsafe_allow_html=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # Navigation Links
    if role == "cyber":
        st.page_link("pages/1_Cyber_Incidents.py", label="🔐 Cyber Dashboard")

    if role == "data":
        st.page_link("pages/2_Datasets.py", label="📁 Data Dashboard")

    if role == "it":
        st.page_link("pages/3_IT_Tickets.py", label="🛠 IT Dashboard")

    # Logout Button
    if st.button(" Logout", key="logout_btn", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.role = None
        st.switch_page("pages/0_Login.py")

# -------------------------------------------------------------------
# MAIN PAGE CONTENT
# -------------------------------------------------------------------
st.markdown(
    "<h1 style='color:white;'> Welcome to the Intelligence Platform</h1>",
    unsafe_allow_html=True
)

if role == "cyber":
    st.success("You have **Cybersecurity** access.")

elif role == "data":
    st.success("You have **Data Analyst** access.")

elif role == "it":
    st.success("You have **IT Operations** access.")

st.write("Use the navigation sidebar to access your tools and dashboards.")
