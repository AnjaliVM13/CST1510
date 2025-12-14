"""
Profile Settings Page
Allows users to upload and manage their profile picture.
Features avatar preview with animated ring and image upload functionality.
"""

import streamlit as st
from pathlib import Path
from PIL import Image
import base64
# Import sidebar and theme components
from app.components.sidebar import render_sidebar
from app.dashboard_theme import apply_cyberpunk_dashboard_theme

# Apply cyberpunk theme styling
apply_cyberpunk_dashboard_theme()

# Render sidebar with user profile
render_sidebar()

# ==============================
# CUSTOM "GAMING" FONTS
# ==============================
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&display=swap');

.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5 {
    font-family: 'Orbitron', sans-serif;
    color: #ffffff;
    text-shadow: 0 0 5px #ff33ff, 0 0 10px #ff33ff, 0 0 20px #ff33ff, 0 0 30px #bb00ff;
    font-size: 33px;
}

.stApp p, .stApp label, .stApp div {
    font-family: 'Orbitron', sans-serif;
    color: #e0e0e0;
}

.metric-card {
    font-family: 'Orbitron', sans-serif;
    background: rgba(20,0,30,0.6);
    border-radius: 12px;
    padding: 25px 20px;
    color: #ffffff;
    text-align: center;
    box-shadow: 0 0 15px rgba(255,0,255,0.5);
    transition: 0.3s;
    min-width: 240px;
    margin-bottom: 20px;
}

.metric-card:hover {
    box-shadow: 0 0 25px rgba(255,0,255,0.8);
    transform: scale(1.05);
}

.stButton>button {
    font-family: 'Orbitron', sans-serif;
    font-weight: bold;
    color: #ffffff;
    text-shadow: 0 0 3px #ff00ff;
}

.stDataFrame th {
    font-family: 'Orbitron', sans-serif;
    color: #ffffff;
    text-shadow: 0 0 2px #ff33ff;
}

.css-1d391kg p, .css-1d391kg label {
    font-family: 'Orbitron', sans-serif;
    color: #ff33ff;
}
</style>
""",
    unsafe_allow_html=True,
)

st.set_page_config(page_title="Profile Settings", layout="centered")

# Auth check (keep your logic)
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("pages/Close.py")

username = st.session_state.get("username", "user")

# ----------------------------
# Robust assets path (relative to this file)
# ----------------------------
# Locate the project root by going two levels up from this file (pages/<thisfile>)
HERE = Path(__file__).resolve()
PROJECT_ROOT = HERE.parents[1]  # Typically project root directory
# Construct path to profile pictures directory
PROFILE_DIR = PROJECT_ROOT / "assets" / "profile_pics"
# Create directory if it doesn't exist
PROFILE_DIR.mkdir(parents=True, exist_ok=True)
# Construct full path to user's profile picture
PROFILE_PATH = PROFILE_DIR / f"{username}.png"

# ----------------------------
# CSS
# ----------------------------
st.markdown(
    """
<style>
.profile-preview { text-align: center; margin-bottom: 20px; }
.avatar-ring {
    width: 150px; height: 150px; border-radius: 50%;
    padding: 5px; margin: auto;
    display: flex; align-items: center; justify-content: center;
    background: conic-gradient(from 180deg, #6a5acd, #8a2be2, #4f46e5, #6a5acd);
}
.avatar-img {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;      /* Ensures the image fills the circle nicely */
    object-position: center; /* Ensures face stays centered */
    border: 3px solid #0E1117;
    background-color: #111827;
}

</style>
""",
    unsafe_allow_html=True,
)

st.title("👤 Profile Settings")
st.write("Update your avatar and personal settings.")


# ----------------------------
# Helper to convert local image to base64 data URI
# ----------------------------
def img_to_data_uri(p: Path):
    """
    Convert local image file to base64 data URI for embedding in HTML.
    
    Args:
        p: Path to PNG image file
        
    Returns:
        str or None: Data URI string or None if conversion fails
    """
    try:
        # Read file bytes and encode to base64
        b = p.read_bytes()
        encoded = base64.b64encode(b).decode("utf-8")
        # Return data URI format for embedding
        return f"data:image/png;base64,{encoded}"
    except Exception as e:
        # Display warning if file read fails
        st.warning(f"Could not read file for embedding: {e}")
        return None


# ----------------------------
# Show avatar (embedded)
# ----------------------------
st.markdown("<div class='profile-preview'>", unsafe_allow_html=True)
st.markdown("<div class='avatar-ring'>", unsafe_allow_html=True)

if PROFILE_PATH.exists():
    data_uri = img_to_data_uri(PROFILE_PATH)
    if data_uri:
        st.markdown(
            f"<img src='{data_uri}' class='avatar-img'/>", unsafe_allow_html=True
        )
    else:
        # fallback to st.image (should still work)
        try:
            st.image(str(PROFILE_PATH), width=140)
        except Exception:
            st.markdown(
                "<div style='width:140px;height:140px;border-radius:50%;background:#111'></div>",
                unsafe_allow_html=True,
            )
else:
    # default icon - embed remote image (browser will fetch this)
    st.markdown(
        "<img src='https://cdn-icons-png.flaticon.com/512/9131/9131529.png' class='avatar-img'/>",
        unsafe_allow_html=True,
    )

st.markdown("</div></div>", unsafe_allow_html=True)

# ----------------------------
# Upload/Save logic (PIL ensures valid PNG)
# ----------------------------
# File uploader for profile picture (supports JPG, JPEG, PNG)
uploaded_file = st.file_uploader(
    "Upload a new profile picture", type=["jpg", "jpeg", "png"]
)

# Show info message when file is uploaded
if uploaded_file:
    st.info("Preview above updates when you click **Save Changes**.")

# Handle save button click
if st.button("Save Changes"):
    if uploaded_file:
        try:
            # Open uploaded image and convert to RGB (handles RGBA, etc.)
            img = Image.open(uploaded_file).convert("RGB")
            # Save as PNG format for reliability
            img.save(PROFILE_PATH, format="PNG")
            st.success("Profile picture saved.")
            # Rerun to show updated preview
            st.rerun()
        except Exception as e:
            # Display error if image processing fails
            st.error(f"Failed to process image: {e}")
    else:
        # Warn user if no file uploaded
        st.warning("Please upload a picture first!")
