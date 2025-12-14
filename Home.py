"""
Home Dashboard Page - Main landing page after user login.
Displays welcome message, role-based access information, and holographic visual effects.
"""

import streamlit as st
import sys
from pathlib import Path
from streamlit.components.v1 import html

# Import custom sidebar component
from app.components.sidebar import render_sidebar

# Hide Material icon fallback text in sidebar
st.markdown(
    """
    <style>
    /* Hide the Material icon text that appears as fallback */
    [data-testid="stSidebar"] div[data-testid="stExpander"] span {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Render the custom sidebar with user profile and navigation
render_sidebar()


# Ensure Python can find the 'app' folder for imports
sys.path.append(str(Path(__file__).resolve().parent.parent))
from app.theme.dashboard_effects import apply_dashboard_effects


# -------------------------
# PAGE CONFIG FIRST
# -------------------------
# Configure page title and layout before rendering content
st.set_page_config(page_title="Home Dashboard", layout="wide")

# Apply dashboard visual effects (particles, animations, etc.)
apply_dashboard_effects()


# -------------------------
# AUTH CHECK
# -------------------------
# Verify user is logged in, redirect to login if not authenticated
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("pages/Close.py")

# Get current user information from session state
username = st.session_state.username
role = st.session_state.role.lower().strip()  # Normalize role to lowercase


# -------------------------
# GLOBAL CSS (Fonts & Neon Headings)
# -------------------------
# Apply Orbitron font and neon glow effects to all headings
st.markdown(
    """
<style>
/* Import Orbitron font from Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700&display=swap');

/* Apply Orbitron font globally to all elements */
html, body, [class*="css"] {
    font-family: 'Orbitron', sans-serif !important;
}

/* Style headings with white text and purple neon glow effect */
h1, h2, h3, h4, h5 {
    font-family: 'Orbitron', sans-serif !important;
    color: #ffffff !important;
    text-shadow: 0 0 6px #cc00ff, 0 0 12px #cc00ff, 0 0 24px #cc00ff;
}

</style>
""",
    unsafe_allow_html=True,
)

# -------------------------
# HOLOGRAPHIC TITLE EFFECT (TSParticles)
# -------------------------
# Create animated holographic sphere with TSParticles library behind welcome title
html(
    f"""
    <!-- Outer movable box -->
    <div id="titleBox" style="
        position: relative;
        width: 100%;
        display: flex;
        justify-content: center;
        margin-top: -80px;  /* Move the whole box up or down */
    ">
        <!-- Inner container with all content -->
        <div style="
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 600px;       /* Increase if needed for sphere/text */
            text-align: center;
            position: relative;
        ">

            <!-- Load Orbitron font -->
            <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700&display=swap" rel="stylesheet">

            <!-- Force h1 and p to use Orbitron -->
            <style>
                h1, p {{
                    font-family: 'Orbitron', sans-serif !important;
                }}
            </style>

            <!-- Title -->
            <h1 style="
                position: relative;
                z-index: 2;
                color: #ffffff;
                text-shadow:
                    0 0 6px #cc00ff,
                    0 0 12px #cc00ff,
                    0 0 24px #cc00ff,
                    0 0 36px #bb00ff;
                font-size: 48px;
                font-weight: bold;
                text-align: center;
                margin-top: -1px;">
                ✨Welcome to the<span style="display: block;">Intelligence Platform</span>
            </h1>

            <!-- Welcome text -->
            <p style="
                position: relative;
                z-index:2;
                color:#d6d6d6;
                font-size:18px;
                margin-top: -10px;">
                Welcome <strong>{username}</strong> — Role: <strong>{role}</strong>
            </p>

            <!-- TSParticles sphere behind title -->
            <div id="holoSphereHome" style="
                position:absolute;
                top:50%;
                left:50%;
                transform:translate(-50%, -50%);
                width:450px;
                height:450px;
                z-index:1;">
            </div>

        </div>
    </div>

    <!-- TSParticles script -->
    <script src="https://cdn.jsdelivr.net/npm/tsparticles@2.11.1/tsparticles.bundle.min.js"></script>
    <script>
        tsParticles.load("holoSphereHome", {{
            fullScreen: false,
            background: {{ color: "transparent" }},
            interactivity: {{
                events: {{
                    onHover: {{ enable: true, mode: "repulse" }},
                    onClick: {{ enable: true, mode: "push" }}
                }},
                modes: {{
                    repulse: {{ distance: 120, duration: 0.6 }},
                    push: {{ quantity: 3 }}
                }}
            }},
            particles: {{
                number: {{ value: 80 }},
                size: {{ value: {{ min: 2, max: 6 }} }},
                color: {{ value: ["#cc00ff","#bb00ff","#ff33ff"] }},
                links: {{
                    enable: true,
                    distance: 100,
                    color: "#ff00ff",
                    opacity: 0.35,
                    width: 1.3
                }},
                move: {{ enable: true, speed: 1.4 }}
            }}
        }});
    </script>
    """,
    height=600,  # match or slightly exceed inner container height
)


# -------------------------
# ROLE ALERTS
# -------------------------
# Define color scheme for each user role (neon colors)
role_colors = {"cyber": "#cc00ff", "data": "#33ccff", "it": "#ff33cc"}

# Define access messages for each role
role_messages = {
    "cyber": "You have Cybersecurity access.",
    "data": "You have Data Analyst access.",
    "it": "You have IT Operations access.",
}

# Display role-specific alert if user role is recognized
if role in role_messages:
    st.markdown(
        f"""
    <style>
    @keyframes neonPulse {{
        0%, 100% {{
            box-shadow: 0 0 15px {role_colors[role]},
                        0 0 30px {role_colors[role]},
                        0 0 45px {role_colors[role]};
        }}
        50% {{
            box-shadow: 0 0 25px {role_colors[role]},
                        0 0 50px {role_colors[role]},
                        0 0 75px {role_colors[role]};
        }}
    }}
    .neon-alert {{
        font-family: 'Orbitron', sans-serif;
        color: #ffffff;
        font-size: 22px;
        font-weight: bold;
        text-align: center;
        padding: 20px 60px 20px 60px;
        margin: 0 auto 10px auto;
        max-width: 600px;
        border: 2px solid {role_colors[role]};
        border-radius: 15px;
        background: rgba(0, 0, 0, 0.25);
        display: block;
        margin-top: -200px;
        animation: neonPulse 2s infinite alternate;
    }}
    .neon-alert-text {{
        font-family: 'Orbitron', sans-serif;
    }}
    </style>

    <div class="neon-alert">
        <span class="neon-alert-text">{role_messages[role]}</span>
    </div>
    <!-- Last instruction line -->
    <p style="
        margin-top:1px;
        color:#d6d6d6;
        font-size:16px;
        font-family:'Orbitron', sans-serif;
        text-align:center;
    ">
        Use the navigation sidebar to access your tools and dashboards.
    </p>

    
    
    """,
        unsafe_allow_html=True,
    )
