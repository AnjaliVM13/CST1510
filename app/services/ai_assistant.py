"""
AI Assistant Service Module
Premium AI assistant with Gemini API integration, streaming responses,
persistent chat history, and dataset-aware intelligence.
"""

# ai_assistant.py

import streamlit as st
import pandas as pd
import time
import google.generativeai as genai
# Chat history persistence functions
from app.data.chat_history import load_chat, save_chat


# -------------------------------------------------------------------
# HELPER: Convert numeric/string timestamps to datetime
# -------------------------------------------------------------------
def fix_all_timestamps(df, date_cols=None):
    """
    Converts numeric or string timestamps to pandas datetime objects.
    Handles milliseconds, seconds, and string date formats automatically.
    
    Args:
        df: DataFrame to process
        date_cols: List of column names to convert (defaults to common date columns)
        
    Returns:
        DataFrame: DataFrame with converted timestamp columns
    """
    df = df.copy()
    # Default date column names if not specified
    if date_cols is None:
        date_cols = ["timestamp", "created_at", "upload_date"]

    # Process each date column
    for col in date_cols:
        if col in df.columns:

            def convert(val):
                """
                Convert single value to datetime, handling multiple formats.
                
                Args:
                    val: Value to convert (int, float, or string)
                    
                Returns:
                    pd.Timestamp or pd.NaT: Converted datetime or Not a Time
                """
                try:
                    # Return NaT for null values
                    if pd.isna(val):
                        return pd.NaT
                    # Numeric timestamps (Unix epoch)
                    if isinstance(val, (int, float)):
                        if val > 1e12:  # milliseconds (13+ digits)
                            return pd.to_datetime(val, unit="ms")
                        elif val > 1e9:  # seconds (10+ digits)
                            return pd.to_datetime(val, unit="s")
                    # String timestamps (ISO format, etc.)
                    return pd.to_datetime(val, errors="coerce")
                except:
                    # Return NaT on any conversion error
                    return pd.NaT

            # Apply conversion function to entire column
            df[col] = df[col].apply(convert)

    return df


# -------------------------------------------------------------------
# Configure Gemini API
# -------------------------------------------------------------------
# Initialize Gemini API with key from Streamlit secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# -------------------------------------------------------------------
# AI Assistant
# -------------------------------------------------------------------


def ai_assistant(
    title="AI Assistant", context_df=None, role_hint=None, primary_key_name=None
):
    """
    Premium AI assistant with:
    - Neon glowing UI
    - Streaming typing effect
    - Sidebar controls (model, temperature, clear chat)
    - Persistent memory per user
    - Dataset-aware intelligence (optional)
    """

    # ================================================================
    # CREATE UNIQUE KEY FOR THIS INSTANCE
    # ================================================================
    # Sanitize title and create unique identifier to prevent session state conflicts
    import hashlib

    # Normalize title for use in session state keys
    title_safe = title.replace(" ", "_").replace("-", "_").lower()
    # Normalize role hint for use in session state keys
    role_safe = (role_hint or "default").replace(" ", "_").replace("-", "_").lower()
    # Create hash from title + role_hint to ensure uniqueness across instances
    combined = f"{title}_{role_hint}_{primary_key_name}"
    title_hash = hashlib.md5(combined.encode()).hexdigest()[:8]
    # Combine sanitized strings with hash for unique key
    unique_key = f"{title_safe}_{role_safe}_{title_hash}"

    # ================================================================
    # IDENTIFY USER (needed for memory)
    # ================================================================
    user_id = st.session_state.get("user_id", "guest")

    # Load persistent chat ONCE when session starts
    if "assistant_chat" not in st.session_state:
        st.session_state.assistant_chat = load_chat(user_id)

    if "initial_greeting_sent" not in st.session_state:
        st.session_state.initial_greeting_sent = False

    # ================================================================
    # SIDEBAR CONTROLS
    # ================================================================
    with st.sidebar:
        st.subheader("⚙️ AI Controls")

        st.metric("Messages", len(st.session_state.assistant_chat))

        model_name = st.selectbox(
            "Gemini Model",
            ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-pro"],
            index=0,
            key=f"ai_assistant_model_{unique_key}",  # Unique key
        )

        temperature = st.slider(
            "Temperature",
            0.0,
            2.0,
            1.0,
            0.1,
            help="Higher = more creative",
            key=f"ai_assistant_temp_{unique_key}",  # Unique key
        )

        # Clear chat
        if st.button(
            "🗑 Clear Chat",
            use_container_width=True,
            key=f"ai_assistant_clear_{unique_key}",
        ):
            st.session_state.assistant_chat = []
            st.session_state.initial_greeting_sent = False
            save_chat([], user_id)
            st.rerun()

    # ================================================================
    # GLOBAL CSS THEME (Neon Purple)
    # ================================================================
    st.markdown(
        """
    <style>
    body { background-color: #0d0d16; }

    .neon-title {
        font-size: 38px;
        font-weight: 700;
        text-align: center;
        color: #d6b6ff;
        padding: 22px 40px;
        border-radius: 18px;
        background: #13131f;
        box-shadow: 0 0 25px #7b2ff7aa;
        border: 1px solid #7b2ff744;
        margin-bottom: 35px;
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

    # ================================================================
    # TITLE
    # ================================================================
    st.markdown(f"<div class='neon-title'>🤖 {title}</div>", unsafe_allow_html=True)

    # ================================================================
    # FIRST GREETING
    # ================================================================
    # Only add greeting if it doesn't already exist in chat history
    if not any(
        msg["role"] == "assistant" and "Hello! I'm your AI Assistant" in msg["content"]
        for msg in st.session_state.assistant_chat
    ):
        welcome_text = "Hello! I'm your AI Assistant. How can I help you today?"
        st.session_state.assistant_chat.append(
            {"role": "assistant", "content": welcome_text}
        )
        save_chat(st.session_state.assistant_chat, user_id)

    # ================================================================
    # SHOW CHAT HISTORY
    # ================================================================
    for msg in st.session_state.assistant_chat:
        bubble_class = "bubble-user" if msg["role"] == "user" else "bubble-ai"
        st.markdown(
            f"<div class='{bubble_class}'>{msg['content']}</div>",
            unsafe_allow_html=True,
        )

    # ================================================================
    # USER INPUT
    # ================================================================
    user_input = st.chat_input(
        "Ask your question...", key=f"ai_assistant_input_{unique_key}"
    )

    if not user_input:
        return

    st.session_state.assistant_chat.append({"role": "user", "content": user_input})
    st.markdown(f"<div class='bubble-user'>{user_input}</div>", unsafe_allow_html=True)

    # ================================================================
    # BUILD CONVERSATION FOR GEMINI
    # ================================================================
    conversation_text = "You are a helpful assistant.\n\n"
    for msg in st.session_state.assistant_chat:
        role = "User" if msg["role"] == "user" else "Assistant"
        conversation_text += f"{role}: {msg['content']}\n"

    # ================================================================
    # DATASET-AWARE PROMPT (if context_df exists)
    # ================================================================
    if isinstance(context_df, pd.DataFrame) and not context_df.empty:
        # --- Fix timestamps first ---
        context_df = fix_all_timestamps(context_df)

        # --- Format timestamps for AI ---
        timestamp_cols = ["timestamp", "created_at", "upload_date"]
        for col in timestamp_cols:
            if col in context_df.columns:
                context_df[col] = context_df[col].dt.strftime("%Y-%m-%d %H:%M:%S")

        # --- Sort DataFrame by primary key (lowest ID first) ---
        if role_hint == "dataset" and "dataset_id" in context_df.columns:
            # Convert to string for consistent sorting
            context_df["dataset_id"] = context_df["dataset_id"].astype(str)
            context_df = context_df.sort_values(
                "dataset_id", ascending=True
            ).reset_index(drop=True)
        elif role_hint == "it_ticket" and "ticket_id" in context_df.columns:
            # Convert to numeric for proper numeric sorting (handles mixed types)
            context_df["ticket_id"] = pd.to_numeric(
                context_df["ticket_id"], errors="coerce"
            )
            context_df = context_df.sort_values(
                "ticket_id", ascending=True
            ).reset_index(drop=True)
        elif "incident_id" in context_df.columns:
            # Convert to string for consistent sorting
            context_df["incident_id"] = context_df["incident_id"].astype(str)
            context_df = context_df.sort_values(
                "incident_id", ascending=True
            ).reset_index(drop=True)

        # Optional: add explicit row numbers for AI reference
        context_df["_row_number"] = range(1, len(context_df) + 1)

        # --- Determine entity, primary key, and display fields ---
        if role_hint == "it_ticket":
            entity_name = "Ticket"
            pk_field = primary_key_name if primary_key_name else "ticket_id"
            display_fields = [
                "ticket_id",
                "priority",
                "description",
                "status",
                "assigned_to",
                "created_at",
                "resolution_time_hours",
            ]

        elif role_hint == "dataset":
            entity_name = "Dataset"
            pk_field = primary_key_name if primary_key_name else "dataset_id"
            display_fields = [
                "dataset_id",
                "name",
                "rows",
                "columns",
                "uploaded_by",
                "upload_date",
            ]

        else:  # Cyber incidents
            entity_name = "Incident"
            pk_field = primary_key_name if primary_key_name else "incident_id"
            display_fields = [
                "incident_id",
                "timestamp",
                "severity",
                "category",
                "status",
                "description",
            ]

        # --- Build format rules dynamically ---
        format_text = f"{entity_name} Summary (Row X)<br>--------------------------------------------------------<br>"
        for field in display_fields:
            field_title = field.replace("_", " ").title()
            format_text += f"{field_title}: <value><br>"

        format_text += f"<br>Analysis:<br>Generate a clear and concise paragraph summarizing the {entity_name.lower()} above, highlighting key points and any patterns or notable values.\n\n"
        format_text += "Never use emojis or list bullets.<br>Always keep one field per line using <br> tags.<br>\n\n"

        # --- Append JSON to conversation ---
        conversation_text += (
            "When I ask 'what is in row X', ONLY use the row where _row_number == X.\n"
        )
        conversation_text += (
            f"FORMAT RULES FOR {entity_name.upper()} RESPONSES:\n{format_text}\nDataset (JSON):\n"
            + context_df.to_json(orient="records")
            + "\n"
        )

    # ================================================================
    # HELPER: Convert JSON → Human-readable (optional pretty formatting)
    # ================================================================
    def convert_json_to_human(text):
        import json
        from datetime import datetime

        def fix_ts(value):
            try:
                if isinstance(value, (int, float)):
                    if value > 10**12:  # milliseconds
                        return datetime.fromtimestamp(value / 1000).strftime(
                            "%Y-%m-%d %H:%M:%S:%f"
                        )
                    elif value > 10**9:
                        return datetime.fromtimestamp(value).strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                return value
            except:
                return value

        def severity_badge(level):
            colors = {
                "critical": "🔴 **Critical**",
                "high": "🟠 High",
                "medium": "🟡 Medium",
                "low": "🟢 Low",
            }
            return colors.get(str(level).lower(), level.title())

        try:
            if "{" in text and "}" in text:
                json_str = text[text.index("{") : text.rindex("}") + 1]
                parsed = json.loads(json_str)

                if isinstance(parsed, dict):
                    parsed = {k: fix_ts(v) for k, v in parsed.items()}
                    out = "### 🧾 Detailed Row Summary\n\n"
                    for k, v in parsed.items():
                        key = k.replace("_", " ").title()
                        if k == "severity":
                            v = severity_badge(v)
                        out += f"- **{key}:** {v}\n"
                    return out

                if isinstance(parsed, list) and isinstance(parsed[0], dict):
                    df = pd.DataFrame(parsed)
                    for col in df.columns:
                        df[col] = df[col].apply(fix_ts)
                    return (
                        "### 📊 Table Summary\nA structured view of the dataset:\n\n"
                        + df.to_markdown(index=False)
                    )

        except Exception:
            pass

        return text

    # ================================================================
    # SEND TO GEMINI (with retry logic for quota errors)
    # ================================================================
    model = genai.GenerativeModel(model_name)

    max_retries = 3
    retry_delay = 15  # Start with 15 seconds
    ai_text = None

    for attempt in range(max_retries):
        try:
            response = model.generate_content(
                conversation_text, generation_config={"temperature": temperature}
            )
            ai_text = convert_json_to_human(response.text)
            break  # Success, exit retry loop
        except Exception as e:
            error_str = str(e)

            # Check if it's a quota error (429)
            if (
                "429" in error_str
                or "quota" in error_str.lower()
                or "Quota exceeded" in error_str
            ):
                if attempt < max_retries - 1:  # Not the last attempt
                    # Extract retry delay from error if available
                    import re

                    retry_match = re.search(r"retry.*?(\d+)\s*[sS]", error_str)
                    if retry_match:
                        retry_delay = (
                            int(retry_match.group(1)) + 2
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
                    ai_text = (
                        f"⚠️ **Quota Exceeded**\n\n"
                        f"Your Gemini API quota has been exceeded. Please:\n"
                        f"1. **Wait 15-30 minutes** and try again\n"
                        f"2. **Use a different Google account** for a fresh quota\n"
                        f"3. **Check your usage**: https://ai.dev/usage?tab=rate-limit\n\n"
                        f"Error details: {error_str[:200]}"
                    )
            else:
                # Non-quota error, don't retry
                ai_text = f"⚠️ AI Error: {e}"
                break

    if ai_text is None:
        ai_text = "⚠️ Failed to get AI response after multiple attempts."

    # ================================================================
    # STREAMING OUTPUT (WORD-BY-WORD)
    # ================================================================
    placeholder = st.empty()
    full_output = ""
    words = ai_text.split(" ")

    for word in words:
        full_output += word + " "
        placeholder.markdown(
            f"<div class='bubble-ai'>{full_output}<span class='typing-cursor'></span></div>",
            unsafe_allow_html=True,
        )
        time.sleep(0.08)  # adjust speed here

    # Final clean bubble without cursor
    placeholder.markdown(
        f"<div class='bubble-ai'>{full_output}</div>", unsafe_allow_html=True
    )

    # Save assistant reply
    st.session_state.assistant_chat.append(
        {"role": "assistant", "content": full_output}
    )
    save_chat(st.session_state.assistant_chat, user_id)
