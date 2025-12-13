import streamlit as st
from pathlib import Path
import base64


def to_base64(path):
    """Convert file to base64 string."""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


class Sidebar:
    """Sidebar component with glass UI, avatar ring, profile picture, animations, and role-aware theme."""

    def __init__(self):
        """Initialize Sidebar component."""
        self.base_dir = Path(__file__).resolve().parent.parent.parent
        self.profile_dir = self.base_dir / "assets/profile_pics"
        self.role_colors = {
            "CYBER": "role-cyber",
            "DATA": "role-data",
            "IT": "role-it",
            "ADMIN": "role-admin",
        }

    def get_user_info(self):
        """Get user information from session state."""
        username = (st.session_state.get("username") or "User").title()
        role = st.session_state.get("role", "User")
        role = role.upper() if role else "USER"
        return username, role

    def get_avatar_url(self, username):
        """Get avatar URL for user."""
        profile_path = self.profile_dir / f"{username}.png"

        if profile_path.exists():
            return f"data:image/png;base64,{to_base64(profile_path)}"
        else:
            return "https://cdn-icons-png.flaticon.com/512/9131/9131529.png"

    def inject_css(self):
        """Inject custom CSS styles."""
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

    /* --- THEMED LOGOUT BUTTON --- */
    .logout-btn {{
        position: absolute; /* pin at bottom */
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        width: 90%;
        text-align: center;
    }}

    .logout-btn button {{
        background: linear-gradient(135deg, #6a5acd, #4f46e5); /* purple/blue gradient */
        color: white !important;
        width: 100% !important;
        padding: 12px 0 !important;
        border-radius: 12px !important;
        border: none !important;
        font-weight: 700 !important;
        font-size: 16px;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        box-sizing: border-box !important;
        cursor: pointer;
        box-shadow: 0 0 15px rgba(106, 92, 173, 0.6), 0 4px 15px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
    }}

    .logout-btn button:hover {{
        background: linear-gradient(135deg, #4f46e5, #8b5cf6); /* lighter purple on hover */
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.4);
    }}

    .logout-btn button:active {{
        transform: translateY(1px);
        box-shadow: 0 3px 10px rgba(0,0,0,0.2);
    }}


    /* Optional: pin logout button at bottom of sidebar */
    .logout-btn {{
        position: absolute;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
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

    def render_profile_section(self, username, role, avatar_url):
        """Render profile section with avatar and role badge."""
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
        role_class = self.role_colors.get(role, "role-data")

        st.markdown(
            f"<div class='role-badge {role_class}'>🔰 {role}</div>",
            unsafe_allow_html=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("---")

    def render_navigation_links(self, role):
        """Render navigation links based on user role."""
        if role == "CYBER":
            st.page_link("pages/1_Cyber_Incidents.py", label="🔐 Cyber Incidents")

        if role == "DATA":
            st.page_link("pages/2_Datasets.py", label="📁 Data Management")

        if role == "IT":
            st.page_link("pages/3_IT_Tickets.py", label="🛠 IT Tickets")

        st.page_link("pages/4_AI_Assistant.py", label="🤖 Global AI Assistant")
        st.page_link("pages/Profile.py", label="👤 Profile Settings")
        st.markdown("---")

    def render_logout_button(self):
        """Render logout button."""
        with st.sidebar:
            st.markdown(
                """
        <div class='logout-btn'>
            <form action="?logout=true" method="get">
                <button type="submit">Logout</button>
            </form>
        </div>
        """,
                unsafe_allow_html=True,
            )

    def handle_logout(self):
        """Handle logout action."""
        if st.query_params.get("logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.role = None
            st.experimental_rerun()

    def render(self):
        """Render the complete sidebar."""
        username, role = self.get_user_info()
        avatar_url = self.get_avatar_url(username)

        self.inject_css()

        with st.sidebar:
            self.render_profile_section(username, role, avatar_url)
            self.render_navigation_links(role)

        self.render_logout_button()
        self.handle_logout()


# Backward compatibility wrapper function
def render_sidebar():
    """Ultra-modern Sidebar with glass UI, avatar ring, profile picture,
    animations, and role-aware theme - backward compatibility."""
    sidebar = Sidebar()
    sidebar.render()
