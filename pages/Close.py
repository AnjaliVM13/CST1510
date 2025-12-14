"""
Login/Registration Page
Handles user authentication, registration, and session initialization.
Features animated background, particle effects, and glass-morphism UI.
"""

import os
import time
import streamlit as st
from pathlib import Path
# Database connection and user services
from app.data.db import connect_database
from app.services.user_service import register_user, login_user
from app.data.chat_history import load_chat
from app.theme_base import apply_ultimate_dark_theme
from streamlit.components.v1 import html

# Apply the futuristic dark theme with animations
apply_ultimate_dark_theme()


# -------------------------------
# FULL-PAGE ANIMATED BACKGROUND
# -------------------------------
st.markdown(
    """
    <style>
    /* Full-page animated gradient background */
    body, .stApp {
        background: linear-gradient(-45deg, #0a0010, #1a001a, #2a0022, #000000);
        background-size: 400% 400%;
        animation: gradientBG 30s ease infinite;
    }

    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------
st.set_page_config(
    page_title="Login Portal", layout="centered", initial_sidebar_state="collapsed"
)

# ------------------------------------------------------
# HIDE STREAMLIT DEFAULT UI
# ------------------------------------------------------
st.markdown(
    """
<style>
header, footer, #MainMenu {visibility: hidden !important;}
[data-testid="stSidebar"] { display: none !important; }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&display=swap');

/* APPLY ORBITRON FONT GLOBALLY */
html, body, [class*="css"] {
    font-family: 'Orbitron', sans-serif !important;
}

/* Increase font size for headings */
h1, h2, h3, h4, h5, h6, .login-title, .stText, .stMarkdown {
    font-family: 'Orbitron', sans-serif !important;
}

/* Inputs and buttons */
input, .stButton>button {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 16px !important;
}

/* Tabs */
.stTabs [role="tab"], .stTabs [aria-selected="true"] {
    font-family: 'Orbitron', sans-serif !important;
    font-size: 16px !important;
}

/* Login title */
.login-title {
    font-size: 44px !important;
    font-weight: 700;
    text-align: center;
    color: #bb00ff;
    text-shadow: 0 0 15px #bb00ff, 0 0 25px #ff33ff;
}
</style>
""",
    unsafe_allow_html=True,
)


# ------------------------------------------------------
# CUSTOM LOGIN CSS (60/30/10 GLOWING PURPLE)
# ------------------------------------------------------
st.markdown(
    """
<style>placeholder.markdown(
    f"<div style='text-align:center; font-weight:bold; font-family:Orbitron, sans-serif; font-size:18px;'>{typed_text}</div>",
    unsafe_allow_html=True,
)


@keyframes bgPulse {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}


/* FLOATING PARTICLES */
.particle {
    position: fixed;
    width: 6px;
    height: 6px;
    background: #bb00ff33;
    border-radius: 50%;
    animation: floatUp 12s infinite ease-in;
}
@keyframes floatUp {
    0% {transform: translateY(0); opacity: 0;}
    20% {opacity: 1;}
    100% {transform: translateY(-1000px); opacity: 0;}
}

/* GLASS LOGIN BOX */
.login-box {
    background: rgba(26,11,60,0.8); /* darker and more intense */
    backdrop-filter: blur(18px);
    border-radius: 22px;
    padding: 45px;
    width: 440px;
    margin: auto;
    border: 1px solid rgba(187,0,255,0.8); /* stronger border glow */
    box-shadow: 0 0 70px rgba(187,0,255,0.7); /* stronger glow */
    animation: boxGlow 3s ease-in-out infinite alternate;
}

@keyframes boxGlow {
    0% { box-shadow: 0 0 50px rgba(187,0,255,0.4); }
    100% { box-shadow: 0 0 90px rgba(187,0,255,0.8); }
}

/* TITLE */
.login-title {
    text-align: center;
    font-size: 32px;
    color: #bb00ff;
    margin-bottom: 20px;
    font-weight: 700;
    text-shadow: 0 0 15px #bb00ff, 0 0 25px #ff33ff;
}

/* LOGO NEON GLOW */
.logo-neon {
    border-radius: 50%;
    box-shadow: 0 0 20px #bb00ff, 0 0 40px #ff33ff;
}

/* INPUTS */
input {
    background-color: rgba(255,255,255,0.05) !important;
    color: white !important;
    border-radius: 10px !important;
    border: 1px solid rgba(187,0,255,0.3) !important;
}
input:focus {
    border: 1px solid #bb00ff !important;
    box-shadow: 0 0 10px #bb00ff;
}

/* BUTTONS */
.stButton>button {
    background: linear-gradient(135deg, #bb00ff, #ff33ff);
    color: white;
    font-weight: 600;
    border-radius: 12px;
    padding: 12px;
    width: 100%;
    border: none;
    box-shadow: 0 0 20px #bb00ff;
    transition: all 0.3s ease-in-out;
}
.stButton>button:hover {
    background: linear-gradient(135deg, #ff33ff, #bb00ff);
    transform: scale(1.05);
    box-shadow: 0 0 30px #bb00ff, 0 0 50px #ff33ff;
}

/* TABS */
.stTabs [role="tab"] {
    background: transparent; /* remove pale rectangle */
    color: #EEE;
}
.stTabs [aria-selected="true"] {
    background: #bb00ff; /* glowing selected tab */
    color: white;
}
</style>
""",
    unsafe_allow_html=True,
)

# ------------------------------------------------------
# FLOATING PARTICLES
# ------------------------------------------------------
for i in range(25):
    st.markdown(
        f"<div class='particle' style='left:{i*4}%; animation-delay:{i*0.4}s'></div>",
        unsafe_allow_html=True,
    )


# ------------------------------------------------------
# FLOATING NEON SHAPES BEHIND LOGIN BOX
# ------------------------------------------------------
for i, color in enumerate(["#bb00ff", "#ff33ff", "#ffffff"]):
    st.markdown(
        f"<div style='position:fixed; top:{10+i*25}%; left:{5+i*30}%; width:{30+i*10}px; height:{30+i*10}px; border-radius:50%; background:{color}; opacity:0.2; animation: float{i} {6+i*2}s ease-in-out infinite alternate;'></div>",
        unsafe_allow_html=True,
    )

st.markdown(
    """
<style>
#networkSphere {
    animation: rotateSphere 20s linear infinite;
}
@keyframes rotateSphere {
    0% { transform: translateX(-50%) rotateY(0deg); }
    100% { transform: translateX(-50%) rotateY(360deg); }
}

@keyframes float0 {0%{transform:translateY(0);}50%{transform:translateY(25px) translateX(10px);}100%{transform:translateY(0);}}
@keyframes float1 {0%{transform:translateY(0);}50%{transform:translateY(-35px) translateX(-15px);}100%{transform:translateY(0);}}
@keyframes float2 {0%{transform:translateY(0);}50%{transform:translateY(20px) translateX(-10px);}100%{transform:translateY(0);}}
</style>
""",
    unsafe_allow_html=True,
)

# ------------------------------------------------------
# TS PARTICLES NETWORK (NEON LINES)
# ------------------------------------------------------
html(
    """
<div id="tsparticles"></div>
<script src="https://cdn.jsdelivr.net/npm/tsparticles@2.11.1/tsparticles.bundle.min.js"></script>
<script>
tsParticles.load("tsparticles", {
  fullScreen: { enable: true },
  particles: { 
    number: { value: 60 },
    color: { value: ["#bb00ff","#ff33ff","#ffffff"] },
    shape: { type: "circle" },
    opacity: { value: 0.6 },
    size: { value: { min: 1, max: 3 } },
    links: { enable: true, distance: 120, color: "#bb00ff", opacity: 0.3, width: 1 },
    move: { enable: true, speed: 0.4 }
  },
  interactivity: { events: { onHover: { enable: true, mode: "repulse" }, onClick: { enable: true, mode: "push" } } }
});
</script>
""",
    height=0,
)


# ------------------------------------------------------
# CONNECT TO DATABASE
# ------------------------------------------------------
# Establish database connection for user authentication
DB_PATH = Path("DATA/intelligence_platform.db")
conn = connect_database(DB_PATH)

# ------------------------------------------------------
# SESSION STATE
# ------------------------------------------------------
# Initialize session state variables for authentication
for key in ["logged_in", "username", "role"]:
    if key not in st.session_state:
        # Set logged_in to False, others to None
        st.session_state[key] = None if key != "logged_in" else False

# ---------------------------
# HOLOGRAPHIC FLOATING SPHERE
# ---------------------------
html(
    """
<div id="networkSphere" style="position:fixed; top:20%; left:50%; transform:translateX(-50%); width:300px; height:300px; z-index:-1;"></div>
<script src="https://cdn.jsdelivr.net/npm/tsparticles@2.11.1/tsparticles.bundle.min.js"></script>
<script>
tsParticles.load("networkSphere", {
    fullScreen: false,
    background: { color: "transparent" },
    particles: {
        number: { value: 60 },
        color: { value: ["#bb00ff","#ff33ff"] },
        shape: { type: "circle" },
        size: { value: { min: 2, max: 5 } },
        links: { enable: true, distance: 80, color: "#bb00ff", opacity: 0.3, width: 1 },
        move: { enable: true, speed: 1, direction: "none", outModes: "bounce" }
    },
    interactivity: { events: { onHover: { enable: true, mode: "repulse" } } }
});
</script>
""",
    height=300,
)
st.markdown("<div class='login-box-fixed'>", unsafe_allow_html=True)
st.markdown(
    "<h2 class='login-title'>Multi-Domain Intelligence Platform Login</h2>",
    unsafe_allow_html=True,
)

# ------------------------------------------------------
# LOGIN + REGISTER TABS
# ------------------------------------------------------
tabs = st.tabs([" Login", " Register"])

# ======================================
# LOGIN TAB
# ======================================
with tabs[0]:
    # Placeholder for typing effect animation
    placeholder = st.empty()

    # Text to display with typing effect
    welcome_text = "Welcome! Please log in or register to continue."

    # Create typing animation effect
    typed_text = ""
    for char in welcome_text:
        typed_text += char
        # Update placeholder with progressively longer text
        placeholder.markdown(
            f"<div style='text-align:center; font-weight:bold;'>{typed_text}</div>",
            unsafe_allow_html=True,
        )
        time.sleep(0.04)  # Delay between characters for typing effect

    # User input fields for login credentials
    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input(
        "Password", type="password", placeholder="Enter your password"
    )
    
    # Handle login button click
    if st.button("Login", use_container_width=True):
        # Authenticate user credentials
        success, role = login_user(conn, username, password)
        if success:
            # Set session state for authenticated user
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = role
            st.session_state.user_id = username
            # Load user's chat history
            st.session_state.assistant_chat = load_chat(username)
            st.session_state.initial_greeting_sent = False
            st.session_state.assistant_chat_user = username
            st.success(f"Welcome back, {username}! Redirecting...")
            # Redirect to role-specific dashboard
            if role == "cyber":
                st.switch_page("pages/1_Cyber_Incidents.py")
            elif role == "data":
                st.switch_page("pages/2_Datasets.py")
            elif role == "it":
                st.switch_page("pages/3_IT_Tickets.py")
        else:
            # Display error message if login fails
            st.error(role)
    st.markdown("</div>", unsafe_allow_html=True)

# ======================================
# REGISTER TAB
# ======================================
with tabs[1]:
    # User registration input fields
    reg_user = st.text_input("Choose Username")
    reg_pass = st.text_input("Choose Password", type="password")
    reg_role = st.selectbox(
        "Select Your Role", ["Cyber Security", "Data Analyst", "IT Support"]
    )
    
    # Handle registration button click
    if st.button("Register", use_container_width=True):
        # Register new user with provided credentials
        success, msg = register_user(conn, reg_user, reg_pass, reg_role)
        if success:
            st.success("Account successfully created. You can now log in.")
        else:
            # Display error message if registration fails
            st.error(msg)
    st.markdown("</div>", unsafe_allow_html=True)
