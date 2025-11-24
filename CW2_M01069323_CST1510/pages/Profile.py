import streamlit as st
from pathlib import Path
import shutil
from app.components.sidebar import render_sidebar
render_sidebar()
# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------
st.set_page_config(
    page_title="Profile Settings",
    layout="centered"
)

# -------------------------------------------------------
# AUTH CHECK
# -------------------------------------------------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("pages/0_Login.py")

username = st.session_state.get("username", "user")

# Directory for storing profile pictures
PROFILE_DIR = Path("assets/profile_pics")
PROFILE_DIR.mkdir(parents=True, exist_ok=True)

PROFILE_PATH = PROFILE_DIR / f"{username}.png"

# Load existing picture if available
existing_pic = PROFILE_PATH if PROFILE_PATH.exists() else None

# -------------------------------------------------------
# PAGE STYLE
# -------------------------------------------------------
st.markdown("""
<style>

h2, h3, h4, p {
    color: white !important;
}

.profile-preview {
    text-align: center;
    margin-bottom: 20px;
}

.avatar-ring {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    padding: 5px;
    margin: auto;
    background: conic-gradient(
        from 180deg,
        #6a5acd,
        #8a2be2,
        #4f46e5,
        #6a5acd
    );
}

.avatar-img {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    border: 3px solid #0E1117;
    background-color: #1f2937;
    object-fit: cover;
}

.save-btn button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 600;
    width: 100%;
    margin-top: 20px;
}
.save-btn button:hover {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# PAGE CONTENT
# -------------------------------------------------------
st.title("👤 Profile Settings")

st.write("Update your avatar and personal settings.")

# ------------------ PROFILE PICTURE PREVIEW ------------------
st.markdown("<div class='profile-preview'>", unsafe_allow_html=True)

st.markdown("<div class='avatar-ring'>", unsafe_allow_html=True)

if existing_pic:
    st.image(str(existing_pic), use_column_width=True, output_format="PNG")
else:
    st.image("https://cdn-icons-png.flaticon.com/512/9131/9131529.png",
             use_column_width=True)

st.markdown("</div></div>", unsafe_allow_html=True)

# ------------------ UPLOAD NEW PICTURE ------------------
uploaded_file = st.file_uploader("Upload a new profile picture",
                                 type=["jpg", "jpeg", "png"])

# ------------------ SAVE PICTURE ------------------
if uploaded_file:
    st.info("Preview above updates when you click **Save Changes**.")

if st.button("Save Changes"):
    if uploaded_file:
        # Save file to assets/profile_pics/<username>.png
        with open(PROFILE_PATH, "wb") as f:
            shutil.copyfileobj(uploaded_file, f)

        st.success("Profile picture updated successfully!")
        st.rerun()
    else:
        st.warning("Please upload a picture first!")
