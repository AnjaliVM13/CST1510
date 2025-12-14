"""
Global AI Assistant Page
Provides unified AI assistant interface with access to all database entities.
Features Gemini API integration, persistent chat history, and comprehensive data context.
Available to all authenticated users regardless of role.
"""

import streamlit as st
import pandas as pd
import google.generativeai as genai
import time
import sys
import re
from pathlib import Path
from streamlit.components.v1 import html

# Make sure Python can find the 'app' folder BEFORE importing from it
sys.path.append(str(Path(__file__).resolve().parent.parent))
# Import sidebar, database, and data access components
from app.components.sidebar import render_sidebar
from app.data.db import connect_database
from app.data.incidents import get_all_incidents
from app.data.tickets import get_all_tickets
from app.data.datasets import Dataset

# Render sidebar with user profile and navigation
render_sidebar()

# =====================================================
# ACCESS CONTROL
# =====================================================
# Initialize session state variables for authentication
st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("username", None)
st.session_state.setdefault("role", None)

# Redirect to login if not authenticated
if not st.session_state.logged_in:
    st.switch_page("pages/Close.py")

# =====================================================
# DATABASE CONNECTION
# =====================================================
# Establish database connection for data access
DB_PATH = Path("DATA/intelligence_platform.db")
conn = connect_database(DB_PATH)


def fix_ts(val):
    """
    Convert timestamp value to pandas datetime, handling multiple formats.
    
    Args:
        val: Timestamp value (int, float, or string)
        
    Returns:
        pd.Timestamp, pd.NaT, or original value: Converted datetime or original if conversion fails
    """
    try:
        # Return NaT for null values
        if pd.isna(val):
            return pd.NaT
        # Handle numeric timestamps (Unix epoch)
        if isinstance(val, (int, float)):
            # Milliseconds (13+ digits)
            if val > 1e12:
                return pd.to_datetime(val / 1000, unit="s")
            # Seconds (10+ digits)
            if val > 1e9:
                return pd.to_datetime(val, unit="s")
        # String date format (ISO, etc.)
        return pd.to_datetime(val, errors="coerce")
    except:
        # Return original value if conversion fails
        return val


import streamlit as st
from streamlit.components.v1 import html

# Apply full-page neon particle background
html(
    """
    <style>
    /* Make the canvas cover the whole page */
    #bgCanvas {
        position: fixed;
        top: 0;
        left: 0;
        z-index: -1; /* behind everything */
        width: 100vw;
        height: 100vh;
    }

    body {
        margin: 0;
        background-color: #0d0d16; /* fallback dark background */
        overflow-x: hidden;
    }
    </style>

    <canvas id="bgCanvas"></canvas>

    <script>
        const canvas = document.getElementById('bgCanvas');
        const ctx = canvas.getContext('2d');

        function resizeCanvas() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }

        window.addEventListener('resize', resizeCanvas);
        resizeCanvas();

        const particles = [];
        const numParticles = 80;

        for (let i = 0; i < numParticles; i++) {
            particles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                r: Math.random() * 2 + 1.5,
                dx: (Math.random() - 0.5) * 1.2,
                dy: (Math.random() - 0.5) * 1.2
            });
        }

        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            const maxDistance = 130;

            // Draw connections between close particles
            for (let i = 0; i < numParticles; i++) {
                for (let j = i + 1; j < numParticles; j++) {
                    const dx = particles[i].x - particles[j].x;
                    const dy = particles[i].y - particles[j].y;
                    const dist = Math.sqrt(dx*dx + dy*dy);
                    if (dist < maxDistance) {
                        ctx.strokeStyle = `rgba(255, 0, 255, ${1 - dist / maxDistance})`;
                        ctx.lineWidth = 0.8;
                        ctx.beginPath();
                        ctx.moveTo(particles[i].x, particles[i].y);
                        ctx.lineTo(particles[j].x, particles[j].y);
                        ctx.stroke();
                    }
                }
            }

            // Draw particles
            particles.forEach(p => {
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                ctx.fillStyle = "rgba(255, 0, 255, 0.8)";
                ctx.shadowColor = "#ff33ff";
                ctx.shadowBlur = 8;
                ctx.fill();

                // Move particles
                p.x += p.dx;
                p.y += p.dy;

                // Bounce off edges
                if (p.x < 0 || p.x > canvas.width) p.dx *= -1;
                if (p.y < 0 || p.y > canvas.height) p.dy *= -1;
            });

            requestAnimationFrame(animate);
        }

        animate();
    </script>
    """,
    height=10,  # small height is fine since it's fixed-position
)

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


html(
    """
    <div style="position: relative; width: 100%; height: 200px; overflow: hidden; margin-bottom: -20px;">
        <!-- Gradient background -->
        <div style="
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: linear-gradient(270deg, #ff00ff, #00ffff, #ff00ff);
            background-size: 600% 600%;
            animation: gradientAnimation 15s ease infinite;
            filter: blur(50px);
            z-index: -2;
        "></div>

        <!-- Particle canvas -->
        <canvas id="networkCanvas" width="800" height="200" style="
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            z-index: 0;
        "></canvas>

        <!-- Title -->
        <h1 style="
            position: relative;
            z-index: 1;
            text-align: center;
            color: #d6b6ff;
            font-family: 'Orbitron', sans-serif;
            font-size: 36px;
            text-shadow: 0 0 10px #ff33ff, 0 0 20px #bb00ff;
            margin: 0;
            padding-top: 70px;
        ">
            🤖 AI Assistant — Intelligence Platform
        </h1>
    </div>

    <style>
        @keyframes gradientAnimation {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }
    </style>

    <script>
        const canvas = document.getElementById('networkCanvas');
        const ctx = canvas.getContext('2d');
        const particles = [];
        const numParticles = 40;
        const maxDistance = 120;

        // Initialize particles
        for (let i = 0; i < numParticles; i++) {
            particles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                r: Math.random() * 2 + 1.5,
                dx: (Math.random() - 0.5) * 1,
                dy: (Math.random() - 0.5) * 1
            });
        }

        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Draw connections
            for (let i = 0; i < numParticles; i++) {
                for (let j = i + 1; j < numParticles; j++) {
                    const dx = particles[i].x - particles[j].x;
                    const dy = particles[i].y - particles[j].y;
                    const dist = Math.sqrt(dx*dx + dy*dy);
                    if (dist < maxDistance) {
                        ctx.strokeStyle = `rgba(255, 0, 255, ${1 - dist / maxDistance})`;
                        ctx.lineWidth = 1;
                        ctx.beginPath();
                        ctx.moveTo(particles[i].x, particles[i].y);
                        ctx.lineTo(particles[j].x, particles[j].y);
                        ctx.stroke();
                    }
                }
            }

            // Draw particles
            particles.forEach(p => {
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                ctx.fillStyle = "rgba(255, 0, 255, 0.8)";
                ctx.shadowColor = "#ff33ff";
                ctx.shadowBlur = 8;
                ctx.fill();

                // Move
                p.x += p.dx;
                p.y += p.dy;

                // Bounce
                if (p.x < 0 || p.x > canvas.width) p.dx *= -1;
                if (p.y < 0 || p.y > canvas.height) p.dy *= -1;
            });

            requestAnimationFrame(animate);
        }

        animate();
    </script>
    """,
    height=200,
)


# =====================================================
# GEMINI SETUP
# =====================================================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model_default = genai.GenerativeModel("gemini-2.0-flash")

# =====================================================
# NEON THEME STYLING
# =====================================================
st.markdown(
    """
<style>
body { background-color: #0d0d16; }
.neon-title {
    font-size: 36px;
    font-weight: 700;
    text-align: center;
    color: #d6b6ff;
    padding: 20px 40px;
    border-radius: 16px;
    background: #13131f;
    box-shadow: 0 0 25px #7b2ff7aa;
    border: 1px solid #7b2ff744;
    margin-bottom: 30px;
}
.bubble-user {
    background: linear-gradient(135deg, #3b82f6, #06b6d4);
    padding: 12px 16px;
    color: white;
    border-radius: 14px;
    margin-bottom: 12px;
    width: fit-content;
    max-width: 88%;
    margin-left: auto;
    box-shadow: 0 0 12px #1e40afaa;
}
.bubble-ai {
    background: linear-gradient(135deg, #8b5cf6, #a855f7);
    padding: 12px 16px;
    color: white;
    border-radius: 14px;
    width: fit-content;
    max-width: 88%;
    margin-bottom: 16px;
    box-shadow: 0 0 15px #9333ea88;
}
.typing-cursor {
    display: inline-block;
    width: 8px;
    height: 20px;
    background: white;
    margin-left: 4px;
    animation: blink 0.8s infinite;
}
@keyframes blink {
    0% {opacity: 1;}
    50% {opacity: 0;}
    100% {opacity: 1;}
}
</style>
""",
    unsafe_allow_html=True,
)


# =====================================================
# GET USER ROLE
# =====================================================
if "role" not in st.session_state:
    st.error("Role not set. Please login again.")
    st.stop()

user_role = st.session_state.role.lower()


# =====================================================
# LOAD DATA BASED ON ROLE
# =====================================================
def load_role_data(role, conn):
    """Load database data based on user role."""
    role_lower = role.lower() if role else ""
    data = {}

    try:
        if role_lower == "cyber":
            # Load cyber incidents data
            incidents_df = get_all_incidents(conn)
            if not incidents_df.empty:
                data["incidents"] = incidents_df
        elif role_lower == "it":
            # Load IT tickets data
            tickets_df = get_all_tickets(conn)
            if not tickets_df.empty:
                data["tickets"] = tickets_df
        elif role_lower == "data":
            # Load datasets data
            datasets_df = Dataset.get_all(conn)
            if not datasets_df.empty:
                data["datasets"] = datasets_df
    except Exception as e:
        st.warning(f"Could not load data: {str(e)}")

    return data


data_context = load_role_data(user_role, conn)

# =====================================================
# INITIALIZE CHAT HISTORY
# =====================================================
if f"assistant_chat_{user_role}" not in st.session_state:
    st.session_state[f"assistant_chat_{user_role}"] = []

chat_history = st.session_state[f"assistant_chat_{user_role}"]

if f"initial_greeting_{user_role}" not in st.session_state:
    st.session_state[f"initial_greeting_{user_role}"] = False


# =====================================================
# HELPER FUNCTIONS
# =====================================================
def deny_message(role, topic, allowed):
    allowed_str = ", ".join(allowed) if allowed else "None"
    return (
        f"🚫 **Access Denied**\n\n"
        f"Your role **'{role}'** cannot access **'{topic}'** data.\n"
        f"Allowed dashboards: **{allowed_str}**"
    )


def classify_question(question, user_role):
    """Classify question and determine if it's about role-specific data or general."""
    q = question.lower()
    role_lower = user_role.lower() if user_role else ""

    # Check if question is about role-specific data
    if role_lower == "cyber":
        if any(
            w in q
            for w in ["incident", "attack", "breach", "severity", "cyber", "security"]
        ):
            return "incidents"
    elif role_lower == "it":
        if any(
            w in q
            for w in ["ticket", "priority", "open tickets", "it support", "resolution"]
        ):
            return "tickets"
    elif role_lower == "data":
        if any(
            w in q for w in ["dataset", "csv", "data quality", "metadata", "upload"]
        ):
            return "datasets"

    # If not role-specific, it's a general question
    return "general"


def is_allowed(role, topic):
    """Check if user can access this topic."""
    # General questions are always allowed
    if topic == "general":
        return True

    # Check if topic matches user's role
    role_lower = role.lower() if role else ""
    role_topics = {"cyber": ["incidents"], "it": ["tickets"], "data": ["datasets"]}

    allowed_topics = role_topics.get(role_lower, [])
    return topic in allowed_topics


# =====================================================
# INITIAL GREETING
# =====================================================
if not st.session_state[f"initial_greeting_{user_role}"]:
    role_display = user_role.upper() if user_role else "User"
    dashboard_name = {
        "cyber": "Cyber Incidents",
        "it": "IT Tickets",
        "data": "Datasets",
    }.get(user_role.lower(), "Dashboard")

    greeting = f"👋 Hello! I'm your AI Assistant. I can answer general questions and help you with your {dashboard_name} database. What would you like to know?"
    st.markdown(f"<div class='bubble-ai'>{greeting}</div>", unsafe_allow_html=True)
    chat_history.append({"role": "assistant", "content": greeting})
    st.session_state[f"initial_greeting_{user_role}"] = True

# Render previous chat
for msg in chat_history:
    css_class = "bubble-user" if msg["role"] == "user" else "bubble-ai"
    st.markdown(
        f"<div class='{css_class}'>{msg['content']}</div>", unsafe_allow_html=True
    )

# =====================================================
# USER INPUT
# =====================================================
user_q = st.chat_input("Ask me anything:")

if user_q:
    chat_history.append({"role": "user", "content": user_q})
    st.markdown(f"<div class='bubble-user'>{user_q}</div>", unsafe_allow_html=True)

    topic = classify_question(user_q, user_role)

    if not is_allowed(user_role, topic):
        deny_msg = f"🚫 **Access Denied**\n\nI can only answer questions about your {user_role.upper()} dashboard data or general topics. Please ask about {user_role.upper()}-related data or general questions."
        st.markdown(f"<div class='bubble-ai'>{deny_msg}</div>", unsafe_allow_html=True)
        chat_history.append({"role": "assistant", "content": deny_msg})
    else:
        # Get the appropriate data based on topic
        # Map topic to the key in data_context
        topic_key = topic  # incidents, tickets, or datasets
        context_data = data_context.get(topic_key) if topic != "general" else None
        clean_output = ""

        # -------------------
        # ROW-SPECIFIC REQUEST
        # -------------------
        if context_data is not None and (
            "first row" in user_q.lower() or "show first" in user_q.lower()
        ):
            if isinstance(context_data, pd.DataFrame) and not context_data.empty:
                row = context_data.iloc[0].to_dict()
            else:
                st.error("⚠️ No data available for this topic.")
                st.stop()

            # Format row into <br> lines
            row_str = ""
            for k, v in row.items():
                if "time" in k.lower() or "date" in k.lower():
                    v = fix_ts(v)
                    if isinstance(v, pd.Timestamp):
                        v = v.strftime("%B %d %Y, %I:%M:%S %p")

            entity_name = topic.capitalize()
            pk_field = {
                "incidents": "Incident ID",
                "tickets": "Ticket ID",
                "datasets": "Dataset ID",
            }.get(topic, "ID")

            # Strict AI prompt
            prompt = f"""
You are an AI assistant for a cybersecurity intelligence platform.

Use ONLY the following row data exactly as provided. Do NOT invent, change, or add any values.

Row Data:
{row_str}

FORMAT RULES:
- Output exactly as below, using <br> for line breaks.
- Each field must appear exactly as given.
- Include an "Analysis" paragraph strictly based on these row values.
- Do not add emojis, bullet points, or extra fields.

Expected format:
{entity_name} Summary (Row 1)<br>
--------------------------------------------------------<br>
{pk_field}: <value><br>
Timestamp: <value><br>
Severity: <value><br>
Category: <value><br>
Status: <value><br>
Description: <value><br>
Logged At: <value><br>
<br>
Analysis:<br>
A concise paragraph summarizing this {entity_name.lower()} using the exact data above.

User question: {user_q}
"""
            # Retry logic for quota errors
            max_retries = 3
            retry_delay = 15  # Start with 15 seconds
            clean_output = None

            for attempt in range(max_retries):
                try:
                    response = model_default.generate_content(prompt)
                    clean_output = response.text.replace("\n", "<br>")
                    break  # Success, exit retry loop
                except Exception as e:
                    error_str = str(e)

                    # Check if it's a quota error (429)
                    if (
                        "429" in error_str
                        or "quota" in error_str.lower()
                        or "Quota exceeded" in error_str
                        or "ResourceExhausted" in error_str
                    ):
                        if attempt < max_retries - 1:  # Not the last attempt
                            # Extract retry delay from error if available
                            retry_match = re.search(
                                r"retry.*?(\d+\.?\d*)\s*[sS]", error_str
                            )
                            if retry_match:
                                retry_delay = (
                                    int(float(retry_match.group(1))) + 2
                                )  # Add 2 seconds buffer

                            # Show user-friendly message
                            wait_msg = f"⏳ Quota limit reached. Waiting {retry_delay} seconds before retry {attempt + 1}/{max_retries}..."
                            placeholder = st.empty()
                            placeholder.info(wait_msg)
                            time.sleep(retry_delay)
                            placeholder.empty()

                            # Exponential backoff for next retry
                            retry_delay = min(retry_delay * 2, 120)  # Cap at 2 minutes
                        else:
                            # Last attempt failed
                            clean_output = (
                                f"⚠️ **Quota Exceeded**<br><br>"
                                f"Your Gemini API quota has been exceeded. Please:<br>"
                                f"1. Wait a few minutes and try again<br>"
                                f"2. Check your API usage at: https://ai.dev/usage?tab=rate-limit<br>"
                                f"3. Consider upgrading your API plan if needed"
                            )
                            break
                    else:
                        # Non-quota error, don't retry
                        clean_output = f"⚠️ AI Error: {str(e)[:200]}"
                        break

            if clean_output is None:
                clean_output = "⚠️ Failed to get AI response after multiple attempts."

            st.markdown(
                f"<div class='bubble-ai'>{clean_output}</div>", unsafe_allow_html=True
            )
            chat_history.append({"role": "assistant", "content": clean_output})

        # -------------------
        # GENERAL REQUEST
        # -------------------
        else:
            context_text = ""
            if context_data is not None:
                try:
                    if isinstance(context_data, pd.DataFrame):
                        context_text = context_data.to_json(orient="records")
                    elif isinstance(context_data, dict):
                        context_text = str(context_data)
                    else:
                        context_text = str(context_data)
                except:
                    context_text = ""
            with st.spinner("Thinking..."):
                # Build context based on topic
                role_context = ""
                if topic != "general" and context_data is not None:
                    try:
                        if isinstance(context_data, pd.DataFrame):
                            # Provide summary statistics and sample data
                            summary = f"""
Database Summary:
- Total records: {len(context_data)}
- Columns: {', '.join(context_data.columns.tolist())}
- Sample data (first 5 rows): {context_data.head().to_dict(orient='records')}
"""
                            role_context = summary
                        else:
                            role_context = str(context_data)
                    except Exception as e:
                        role_context = (
                            f"Data available but could not be processed: {str(e)}"
                        )

                # Build prompt
                role_name = {
                    "cyber": "Cyber Security",
                    "it": "IT Support",
                    "data": "Data Management",
                }.get(user_role.lower(), "Intelligence Platform")

                if topic == "general":
                    prompt = f"""
You are a helpful AI assistant for a {role_name} Intelligence Platform.

User question: {user_q}

Answer the question helpfully and professionally. If the question is about the platform or general topics, provide a clear and informative answer.
"""
                else:
                    prompt = f"""
You are a helpful AI assistant for a {role_name} Intelligence Platform.

User question: {user_q}

Use the following database information to answer the question accurately:
{role_context}

Provide a clear, helpful answer based on the data. If the data doesn't contain enough information, say so and provide what you can from the available data.
"""

                # Retry logic for quota errors
                max_retries = 3
                retry_delay = 15  # Start with 15 seconds
                ai_text = None

                for attempt in range(max_retries):
                    try:
                        response = model_default.generate_content(prompt)
                        ai_text = response.text
                        break  # Success, exit retry loop
                    except Exception as e:
                        error_str = str(e)

                        # Check if it's a quota error (429)
                        if (
                            "429" in error_str
                            or "quota" in error_str.lower()
                            or "Quota exceeded" in error_str
                            or "ResourceExhausted" in error_str
                        ):
                            if attempt < max_retries - 1:  # Not the last attempt
                                # Extract retry delay from error if available
                                retry_match = re.search(
                                    r"retry.*?(\d+\.?\d*)\s*[sS]", error_str
                                )
                                if retry_match:
                                    retry_delay = (
                                        int(float(retry_match.group(1))) + 2
                                    )  # Add 2 seconds buffer

                                # Show user-friendly message
                                wait_msg = f"⏳ Quota limit reached. Waiting {retry_delay} seconds before retry {attempt + 1}/{max_retries}..."
                                placeholder = st.empty()
                                placeholder.info(wait_msg)
                                time.sleep(retry_delay)
                                placeholder.empty()

                                # Exponential backoff for next retry
                                retry_delay = min(
                                    retry_delay * 2, 120
                                )  # Cap at 2 minutes
                            else:
                                # Last attempt failed
                                ai_text = (
                                    f"⚠️ **Quota Exceeded**\n\n"
                                    f"Your Gemini API quota has been exceeded. Please:\n"
                                    f"1. Wait a few minutes and try again\n"
                                    f"2. Check your API usage at: https://ai.dev/usage?tab=rate-limit\n"
                                    f"3. Consider upgrading your API plan if needed"
                                )
                                break
                        else:
                            # Non-quota error, don't retry
                            ai_text = f"⚠️ AI Error: {str(e)[:200]}"
                            break

                if ai_text is None:
                    ai_text = "⚠️ Failed to get AI response after multiple attempts."

                # Streaming effect
                full_output = ""
                placeholder = st.empty()
                for word in ai_text.split():
                    full_output += word + " "
                    placeholder.markdown(
                        f"<div class='bubble-ai'>{full_output}<span class='typing-cursor'></span></div>",
                        unsafe_allow_html=True,
                    )
                    time.sleep(0.02)
                placeholder.markdown(
                    f"<div class='bubble-ai'>{full_output}</div>",
                    unsafe_allow_html=True,
                )
                chat_history.append({"role": "assistant", "content": full_output})

    st.session_state[f"assistant_chat_{user_role}"] = chat_history

# =====================================================
# CLEAR CHAT BUTTON
# =====================================================
if st.button("🗑 Clear Chat", use_container_width=True):
    st.session_state[f"assistant_chat_{user_role}"] = []
    st.session_state[f"initial_greeting_{user_role}"] = False
    st.rerun()
