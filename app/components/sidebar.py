"""
Sidebar Component Module
Provides a modern glass-morphism sidebar with user profile, role-based navigation, and logout functionality.
"""

import streamlit as st
from pathlib import Path
import base64


def to_base64(path):
    """
    Convert image file to base64 encoded string for embedding in HTML.
    
    Args:
        path: Path to the image file
        
    Returns:
        Base64 encoded string representation of the image
    """
    # Read file in binary mode and encode to base64
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


class Sidebar:
    """Sidebar component with glass UI, avatar ring, profile picture, animations, and role-aware theme."""

    def __init__(self):
        """
        Initialize Sidebar component with base paths and role color mappings.
        Sets up directory paths for profile pictures and CSS class mappings for roles.
        """
        # Get project root directory (3 levels up from this file)
        self.base_dir = Path(__file__).resolve().parent.parent.parent
        # Set profile pictures directory path
        self.profile_dir = self.base_dir / "assets/profile_pics"
        # Map role names to CSS class names for styling
        self.role_colors = {
            "CYBER": "role-cyber",
            "DATA": "role-data",
            "IT": "role-it",
            "ADMIN": "role-admin",
        }

    def get_user_info(self):
        """
        Retrieve and normalize user information from Streamlit session state.
        
        Returns:
            tuple: (username, role) - Username with title case, role in uppercase
        """
        # Get username from session, default to "User" if not found, apply title case
        username = (st.session_state.get("username") or "User").title()
        # Get role from session, default to "User", convert to uppercase
        role = st.session_state.get("role", "User")
        role = role.upper() if role else "USER"
        return username, role

    def get_avatar_url(self, username):
        """
        Get avatar image URL for the specified user.
        Returns base64 encoded local image if exists, otherwise returns default icon URL.
        
        Args:
            username: Username to get avatar for
            
        Returns:
            str: Data URI for local image or URL for default icon
        """
        # Construct path to user's profile picture
        profile_path = self.profile_dir / f"{username}.png"

        # Return base64 encoded image if file exists, otherwise use default icon
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
        """
        Render role-based navigation links in the sidebar.
        Shows only the dashboard relevant to the user's role, plus global pages.
        
        Args:
            role: User's role (CYBER, DATA, IT, or ADMIN)
        """
        # Normalize role to uppercase for consistent comparison
        role_upper = role.upper() if role else ""

        # Display role-specific dashboard link based on user's role
        if role_upper == "CYBER":
            st.page_link("pages/1_Cyber_Incidents.py", label="🔐 Cyber Incidents")
        elif role_upper == "DATA":
            st.page_link("pages/2_Datasets.py", label="📁 Data Management")
        elif role_upper == "IT":
            st.page_link("pages/3_IT_Tickets.py", label="🛠 IT Tickets")
        # Admin role can see all dashboards (if needed in future)
        elif role_upper == "ADMIN":
            st.page_link("pages/1_Cyber_Incidents.py", label="🔐 Cyber Incidents")
            st.page_link("pages/2_Datasets.py", label="📁 Data Management")
            st.page_link("pages/3_IT_Tickets.py", label="🛠 IT Tickets")

        # Global pages available to all users
        st.page_link("pages/4_AI_Assistant.py", label="🤖 Global AI Assistant")
        st.page_link("pages/Profile.py", label="👤 Profile Settings")
        st.markdown("---")  # Visual separator

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
        """
        Handle user logout by clearing session state and rerunning the app.
        Checks for logout query parameter from logout button click.
        """
        # Check if logout was triggered via query parameter
        if st.query_params.get("logout"):
            # Clear authentication and user data from session
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.role = None
            # Rerun app to reflect logout state
            st.experimental_rerun()

    def render(self):
        """
        Main render method that orchestrates the complete sidebar display.
        Gets user info, injects CSS, renders profile, navigation, and logout button.
        """
        # Get current user information
        username, role = self.get_user_info()
        # Get user's avatar image URL
        avatar_url = self.get_avatar_url(username)

        # Inject custom CSS styles
        self.inject_css()

        # Render sidebar content within Streamlit sidebar context
        with st.sidebar:
            # Display user profile section with avatar and role badge
            self.render_profile_section(username, role, avatar_url)
            # Display role-based navigation links
            self.render_navigation_links(role)

        # Render logout button (positioned at bottom)
        self.render_logout_button()
        # Handle logout action if triggered
        self.handle_logout()


# Backward compatibility wrapper function
def render_sidebar():
    """
    Backward compatibility wrapper for sidebar rendering.
    Creates Sidebar instance and renders it.
    
    Ultra-modern Sidebar with glass UI, avatar ring, profile picture,
    animations, and role-aware theme.
    """
    # Create sidebar instance and render
    sidebar = Sidebar()
    sidebar.render()
