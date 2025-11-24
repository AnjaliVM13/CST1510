import streamlit as st
from pathlib import Path
from PIL import Image
import base64
from app.components.sidebar import render_sidebar

render_sidebar()

st.set_page_config(page_title="Profile Settings", layout="centered")

# Auth check (keep your logic)
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("pages/0_Login.py")

username = st.session_state.get("username", "user")

# ----------------------------
# Robust assets path (relative to this file)
# ----------------------------
# We locate the project root by going two levels up from this file (pages/<thisfile>)
HERE = Path(__file__).resolve()
PROJECT_ROOT = HERE.parents[1]    # typically project root
PROFILE_DIR = PROJECT_ROOT / "assets" / "profile_pics"
PROFILE_DIR.mkdir(parents=True, exist_ok=True)
PROFILE_PATH = PROFILE_DIR / f"{username}.png"

# ----------------------------
# CSS
# ----------------------------
st.markdown("""
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
""", unsafe_allow_html=True)

st.title("👤 Profile Settings")
st.write("Update your avatar and personal settings.")

# ----------------------------
# Helper to convert local image to base64 data URI
# ----------------------------
def img_to_data_uri(p: Path):
    """Return data URI for a PNG path. Returns None on failure."""
    try:
        b = p.read_bytes()
        encoded = base64.b64encode(b).decode("utf-8")
        return f"data:image/png;base64,{encoded}"
    except Exception as e:
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
        st.markdown(f"<img src='{data_uri}' class='avatar-img'/>", unsafe_allow_html=True)
    else:
        # fallback to st.image (should still work)
        try:
            st.image(str(PROFILE_PATH), width=140)
        except Exception:
            st.markdown("<div style='width:140px;height:140px;border-radius:50%;background:#111'></div>", unsafe_allow_html=True)
else:
    # default icon - embed remote image (browser will fetch this)
    st.markdown("<img src='https://cdn-icons-png.flaticon.com/512/9131/9131529.png' class='avatar-img'/>", unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)

# ----------------------------
# Upload/Save logic (PIL ensures valid PNG)
# ----------------------------
uploaded_file = st.file_uploader("Upload a new profile picture", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.info("Preview above updates when you click **Save Changes**.")

if st.button("Save Changes"):
    if uploaded_file:
        try:
            img = Image.open(uploaded_file).convert("RGB")
            img.save(PROFILE_PATH, format="PNG")   # reliable PNG
            st.success("Profile picture saved.")
            # show updated debug
            st.rerun()
        except Exception as e:
            st.error(f"Failed to process image: {e}")
    else:
        st.warning("Please upload a picture first!")
