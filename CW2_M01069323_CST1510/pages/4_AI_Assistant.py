import streamlit as st
import google.generativeai as genai
from app.services.data_manager import DataManager
from app.components.sidebar import render_sidebar
render_sidebar()
# --------------------------------------------
# ROLE PERMISSIONS
# --------------------------------------------
ROLE_PERMISSIONS = {
    "cyber": ["incidents", "security", "threats"],
    "data": ["datasets", "data", "analysis"],
    "it": ["tickets", "support", "operations"],
}

st.title("🤖 AI Assistant — Intelligence Platform")

# --------------------------------------------
# LOAD DATABASE (CACHED)
# --------------------------------------------
@st.cache_resource
def load_data():
    return DataManager().load_all()

data_context = load_data()

# --------------------------------------------
# GEMINI SETUP
# --------------------------------------------
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

# --------------------------------------------
# PERMISSION ERROR MESSAGE
# --------------------------------------------
def deny_message(role, topic, required):
    return (
        f"🚫 **Access Denied**\n\n"
        f"Your current role **'{role}'** does not have permission to access **{topic}** data.\n\n"
        f"**Required roles:** {', '.join(required)}"
    )

# --------------------------------------------
# CLASSIFY QUESTION (to detect which topic user is asking)
# --------------------------------------------
def classify_question(question):
    q = question.lower()

    if any(w in q for w in ["incident", "attack", "breach", "severity"]):
        return "incidents"

    if any(w in q for w in ["dataset", "csv", "data quality", "metadata"]):
        return "datasets"

    if any(w in q for w in ["ticket", "priority", "open tickets"]):
        return "tickets"

    return "general"

# --------------------------------------------
# CHECK IF ROLE CAN ACCESS TOPIC
# --------------------------------------------
def is_allowed(role, topic):
    allowed = ROLE_PERMISSIONS.get(role, [])

    if "all" in allowed:
        return True

    return topic in allowed or topic == "general"

# --------------------------------------------
# AI CALL
# --------------------------------------------
def ask_ai(question, context):
    prompt = f"""
You are an AI assistant for a cybersecurity intelligence platform.

Here is the platform data you can use to answer:

{context}

User question:
{question}

If the question is general, answer normally.
If the question is about the database, analyze the available data and give a clear explanation.
"""

    response = model.generate_content(prompt)
    return response.text

# --------------------------------------------
# GET USER ROLE (from login system)
# --------------------------------------------
if "role" not in st.session_state:
    st.error("Role not set. Please login again.")
    st.stop()

user_role = st.session_state.role

# --------------------------------------------
# UI — INPUT
# --------------------------------------------
user_question = st.text_input(
    "Ask me anything (general or about the intelligence platform):"
)

if user_question:
    # Detect what the question refers to
    topic = classify_question(user_question)

    # Permission check
    if not is_allowed(user_role, topic):
        required_roles = [
            r for r, perms in ROLE_PERMISSIONS.items()
            if topic in perms or "all" in perms
        ]
        st.error(deny_message(user_role, topic, required_roles))
        st.stop()

    # Allowed — answer with AI
    with st.spinner("Thinking..."):
        answer = ask_ai(user_question, data_context)

    st.markdown("### 🧠 AI Response")
    st.write(answer)
