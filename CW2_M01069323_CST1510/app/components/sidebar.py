import streamlit as st
from pathlib import Path

def render_sidebar():
    """Ultra-modern Sidebar with glass UI, avatar ring, profile picture,
    animations, and role-aware theme."""

    # -------------------------------------------------------
    # Determine user info
    # -------------------------------------------------------
    username = (st.session_state.get("username") or "User").title()
    role = st.session_state.get("role", "User")
    role = role.upper() if role else "USER"


    # Profile picture path
    PROFILE_PATH = Path("assets/profile_pics") / f"{username.lower()}.png"

    if PROFILE_PATH.exists():
        avatar_url = str(PROFILE_PATH)
    else:
        # Default avatar
        avatar_url = "https://cdn-icons-png.flaticon.com/512/9131/9131529.png"

    # -------------------------------------------------------
    # Inject custom CSS
    # -------------------------------------------------------
    st.markdown(
        f"""
    <style>

    /* --- SIDEBAR GLASS EFFECT --- */
    [data-testid="stSidebar"] {{
        background: rgba(15, 17, 26, 0.55) !important;
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border-right: 1px solid rgba(255,255,255,0.05);
        padding-top: 25px;
    }}

    /* Remove Streamlit default padding */
    .st-emotion-cache-1lcbmhc {{
        padding-top: 0 !important;
    }}

    /* --- PROFILE SECTION --- */
    .profile-box {{
        text-align: center;
        margin-bottom: 20px;
    }}

    /* Glowing gradient ring */
    .avatar-ring {{
        width: 110px;
        height: 110px;
        margin: auto;
        padding: 4px;
        border-radius: 50%;
        background: conic-gradient(
            from 0deg,
            #4f46e5,
            #6a5acd,
            #8b5cf6,
            #4f46e5
        );
        animation: spin 6s linear infinite;
    }}

    /* Spin animation */
    @keyframes spin {{
        from {{ transform: rotate(0deg); }}
        to {{ transform: rotate(360deg); }}
    }}

    /* Actual avatar */
    .avatar-img {{
        width: 100%;
        height: 100%;
        border-radius: 50%;
        border: 3px solid #0E1117;
        object-fit: cover;
        background-color: #111827;
    }}

    /* Username text */
    .username {{
        margin-top: 10px;
        font-size: 20px;
        font-weight: 700;
        color: white;
    }}

    /* Role badge */
    .role-badge {{
        margin-top: 6px;
        padding: 6px 12px;
        font-size: 12px;
        font-weight: 600;
        border-radius: 12px;
        display: inline-block;
    }}

    /* Role colors */
    .role-cyber {{ background: #f43f5e33; color: #f43f5e; }}
    .role-data {{ background: #0ea5e933; color: #0ea5e9; }}
    .role-it   {{ background: #f59e0b33; color: #f59e0b; }}
    .role-admin{{ background: #a855f733; color: #a855f7; }}

    /* --- NAV LINKS HOVER ANIMATION --- */
    .st-emotion-cache-1v0mbdj a:hover {{
        padding-left: 8px;
        transition: 0.2s ease-in-out;
        color: #a78bfa !important;
        font-weight: 600;
    }}

    /* --- FLOATING LOGOUT BUTTON --- */
    .logout-btn button {{
        background: linear-gradient(135deg, #ef4444, #dc2626);
        color: white;
        width: 95%;
        font-weight: 600;
        border-radius: 10px;
        padding: 8px 12px;
        margin-top: 20px;
        margin-left: 5px;
    }}
    .logout-btn button:hover {{
        background: linear-gradient(135deg, #dc2626, #b91c1c);
    }}

    /* Link to Profile Settings */
    .profile-link:hover {{
        padding-left: 4px;
        color: #8b5cf6 !important;
        transition: 0.2s;
    }}

    </style>
    """,
        unsafe_allow_html=True,
    )

    # -------------------------------------------------------
    # Sidebar UI content
    # -------------------------------------------------------
    with st.sidebar:

        # PROFILE HEADER
        st.markdown("<div class='profile-box'>", unsafe_allow_html=True)

        # Avatar ring
        st.markdown(
            f"""
            <div class='avatar-ring'>
                <img class='avatar-img' src='{avatar_url}'>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(f"<div class='username'>{username}</div>", unsafe_allow_html=True)

        # Role badge
        role_class = {
            "CYBER": "role-cyber",
            "DATA": "role-data",
            "IT": "role-it",
            "ADMIN": "role-admin",
        }.get(role, "role-data")

        st.markdown(
            f"<div class='role-badge {role_class}'>🔰 {role}</div>",
            unsafe_allow_html=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")

        # -------------------------------------------------------
        # Navigation Links
        # -------------------------------------------------------
        if role == "CYBER":
            st.page_link("pages/1_Cyber_Incidents.py", label="🔐 Cyber Incidents")

        if role == "DATA":
            st.page_link("pages/2_Datasets.py", label="📁 Data Management")

        if role == "IT":
            st.page_link("pages/3_IT_Tickets.py", label="🛠 IT Tickets")

        st.page_link("pages/4_AI_Assistant.py", label="🤖 Global AI Assistant")

        # Profile settings link
        st.page_link("pages/Profile.py", label="👤 Profile Settings")

        st.markdown("---")

        # -------------------------------------------------------
        # Logout Button
        # -------------------------------------------------------
        st.markdown("<div class='logout-btn'>", unsafe_allow_html=True)
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.role = None
            st.switch_page("pages/0_Login.py")
        st.markdown("</div>", unsafe_allow_html=True)
