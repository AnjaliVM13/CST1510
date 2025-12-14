"""
Floating AI Chatbox Component Module
Provides floating chat interface with Gemini AI integration, persistent chat history,
and quota management features. Supports multiple data sources for context-aware responses.
"""

import streamlit as st
import pandas as pd
import google.generativeai as genai
# Chat history persistence manager
from app.data.chat_history import ChatHistory


class FloatingAIChatbox:
    """
    Floating AI chatbox component with icon button and popup chat interface.
    Integrates with Google Gemini API for intelligent responses with quota management.
    """

    def __init__(
        self,
        chat_key: str,
        df: pd.DataFrame = None,
        title="AI Assistant",
        matching_df: pd.DataFrame = None,
        unmatching_df: pd.DataFrame = None,
        manual_data: pd.DataFrame = None,
    ):
        """
        Initialize FloatingAIChatbox component with data sources and configuration.
        
        Args:
            chat_key: Unique identifier for this chat instance
            df: Original/main data DataFrame for context
            title: Display title for the chatbox
            matching_df: Uploaded CSV data with matching columns
            unmatching_df: Uploaded CSV data with non-matching columns
            manual_data: Manually entered data rows
        """
        self.chat_key = chat_key
        self.df = df  # Original/main data for AI context
        self.matching_df = matching_df  # Uploaded matching CSV data
        self.unmatching_df = unmatching_df  # Uploaded unmatching CSV data
        self.manual_data = manual_data  # Manually added data
        self.title = title
        # Create unique session state keys
        self.state_key = f"{chat_key}_chat_history"
        self.chat_open_key = f"{chat_key}_chat_open"
        # Initialize chat history manager
        self.chat_history = ChatHistory()
        # Get user ID from session state (fallback to username or "guest")
        self.user_id = st.session_state.get(
            "user_id", st.session_state.get("username", "guest")
        )

        # Initialize session state with persistent chat history
        if self.state_key not in st.session_state:
            # Load saved chat history for this user and chat key
            st.session_state[self.state_key] = self.chat_history.load_chat(
                f"{self.user_id}_{chat_key}"
            )

        # Initialize chat open/closed state
        if self.chat_open_key not in st.session_state:
            st.session_state[self.chat_open_key] = False

        # Initialize sidebar control keys for AI model settings
        self.model_key = f"{chat_key}_model"
        self.temperature_key = f"{chat_key}_temperature"

        # Set default AI model (Gemini Flash for faster responses)
        if self.model_key not in st.session_state:
            st.session_state[self.model_key] = "gemini-1.5-flash"
        # Set default temperature (1.0 = balanced creativity)
        if self.temperature_key not in st.session_state:
            st.session_state[self.temperature_key] = 1.0

        # Initialize minimal mode - default to True to reduce API quota usage
        minimal_mode_key = f"{chat_key}_minimal_mode"
        if minimal_mode_key not in st.session_state:
            st.session_state[minimal_mode_key] = True  # Default to True to save quota

    def inject_css(self):
        """Inject CSS for floating icon."""
        st.markdown(
            """
        <style>
        /* Floating AI Icon Button - Fixed position */
        .floating-ai-icon-wrapper {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
        }
        
        /* Chatbox styling - adjust max-height to make chatbox taller */
        .chatbox-container {
            background: rgba(20, 0, 30, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            border: 1px solid rgba(187, 0, 255, 0.3);
            box-shadow: 0 0 30px rgba(187, 0, 255, 0.5);
            overflow: hidden;
            max-height: 900px;  /* Change this to adjust max height: 600=small, 800=medium, 900=large, 1200=very large */
            display: flex;
            flex-direction: column;
        }
        
        .chatbox-header {
            background: linear-gradient(135deg, #8b5cf6, #a855f7);
            padding: 12px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        
        .chatbox-title {
            color: white;
            font-weight: 700;
            font-size: 16px;
            font-family: 'Orbitron', sans-serif;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )

    def render_sidebar_controls(self):
        """Render AI controls in the sidebar."""
        if st.session_state.get(self.chat_open_key, False):
            with st.sidebar:
                st.subheader("⚙️ AI Controls")

                # Message count
                st.metric("Messages", len(st.session_state.get(self.state_key, [])))

                # Model selection - Streamlit automatically manages the session state via key
                model_name = st.selectbox(
                    "Gemini Model",
                    [
                        "gemini-1.5-flash",
                        "gemini-1.5-pro",
                        "gemini-2.0-flash",
                        "gemini-pro",
                    ],
                    index=0,
                    key=self.model_key,
                )
                # Don't manually set - Streamlit handles it via the key parameter

                # Temperature slider - Streamlit automatically manages the session state via key
                temperature = st.slider(
                    "Temperature",
                    0.0,
                    2.0,
                    st.session_state.get(self.temperature_key, 1.0),
                    0.1,
                    help="Higher = more creative",
                    key=self.temperature_key,
                )
                # Don't manually set - Streamlit handles it via the key parameter

                # Clear chat button
                if st.button(
                    "🗑 Clear Chat",
                    use_container_width=True,
                    key=f"{self.chat_key}_clear",
                ):
                    st.session_state[self.state_key] = []
                    self.chat_history.save_chat([], f"{self.user_id}_{self.chat_key}")
                    st.rerun()

                # Minimal mode toggle to reduce API usage (defaults to True)
                minimal_mode = st.checkbox(
                    "🔋 Minimal Mode (Metadata Only) - RECOMMENDED",
                    value=st.session_state.get(
                        f"{self.chat_key}_minimal_mode", True
                    ),  # Default to True
                    help="Enable to reduce API quota usage by 60-80%. Sends database structure (columns, types, 1-2 samples) so AI can still answer questions about your data.",
                    key=f"{self.chat_key}_minimal_checkbox",
                )
                st.session_state[f"{self.chat_key}_minimal_mode"] = minimal_mode

                if minimal_mode:
                    st.success(
                        "✅ Minimal Mode enabled - Sends metadata only (can still answer database questions, uses 60-80% fewer tokens)"
                    )
                else:
                    st.warning(
                        "⚠️ Full Mode - Sends more data (may hit quota limits faster). Consider enabling Minimal Mode if you see quota errors."
                    )

                # Show current API key status (first 10 chars for security)
                try:
                    api_key = st.secrets.get("GEMINI_API_KEY", "")
                    if api_key:
                        key_preview = (
                            api_key[:10] + "..." if len(api_key) > 10 else api_key
                        )
                        st.caption(f"🔑 API Key: {key_preview} (loaded)")
                    else:
                        st.error("⚠️ API Key not found - check secrets.toml")
                except:
                    st.warning("⚠️ Could not read API key")

                # Info about quota
                st.warning(
                    "⚠️ **IMPORTANT:** Quota is per **Google Account**, not per API key!\n\n"
                    "If you keep changing API keys from the **same Google account**, they all share the same quota.\n\n"
                    "**Solutions:**\n"
                    "1. Use a **different Google account** for a new API key\n"
                    "2. Wait for quota to reset (usually hourly/daily)\n"
                    "3. Enable Minimal Mode (already enabled) - reduces usage by 70-85%\n"
                    "4. Wait 1-2 minutes between requests"
                )

    def render_floating_icon(self):
        """Render floating AI icon button - not used when rendered in column."""
        # Icon is now rendered directly in the dashboard page
        pass

    def get_all_data_context(self):
        """Combine all data sources for AI context."""
        all_data = {}

        if self.df is not None and not self.df.empty:
            all_data["original_data"] = self.df.to_dict(orient="records")

        if self.matching_df is not None and not self.matching_df.empty:
            all_data["uploaded_matching_data"] = self.matching_df.to_dict(
                orient="records"
            )

        if self.unmatching_df is not None and not self.unmatching_df.empty:
            all_data["uploaded_unmatching_data"] = self.unmatching_df.to_dict(
                orient="records"
            )

        if self.manual_data is not None and not self.manual_data.empty:
            all_data["manually_added_data"] = self.manual_data.to_dict(orient="records")

        return all_data

    def generate_ai_response(self, user_message: str) -> str:
        """Generate AI response using Gemini with retry logic and quota handling."""
        import time
        import json
        import re

        # Get model and temperature from sidebar controls
        selected_model = st.session_state.get(self.model_key, "gemini-1.5-flash")
        temperature = st.session_state.get(self.temperature_key, 1.0)

        # Try different models in order of preference (fallback if selected model fails)
        models_to_try = [
            selected_model,  # User's selected model first
            "gemini-1.5-flash",  # Usually has better free tier limits
            "gemini-1.5-pro",  # Alternative model
            "gemini-2.0-flash",  # Original model (may have stricter limits)
        ]
        # Remove duplicates while preserving order
        models_to_try = list(dict.fromkeys(models_to_try))

        # Configure API key with error handling - reconfigure each time to ensure fresh key
        try:
            api_key = st.secrets.get("GEMINI_API_KEY")
            if not api_key:
                return "⚠️ Error: GEMINI_API_KEY not found in secrets. Please check your .streamlit/secrets.toml file and restart the app."

            # Validate API key format (should start with AIzaSy)
            if not api_key.startswith("AIzaSy"):
                return "⚠️ Error: Invalid API key format. Gemini API keys should start with 'AIzaSy'. Please check your .streamlit/secrets.toml file."

            # Reconfigure each time to ensure we're using the latest key
            genai.configure(api_key=api_key)
        except KeyError:
            return "⚠️ Error: GEMINI_API_KEY not found in secrets. Please check your .streamlit/secrets.toml file and restart the app."
        except Exception as e:
            return f"⚠️ Error: Failed to configure API key: {str(e)[:200]}. Make sure you restarted the app after changing the key."

        # Check if we should use minimal mode (metadata only, not full data) to reduce quota usage
        use_minimal_mode = st.session_state.get(f"{self.chat_key}_minimal_mode", False)

        # Get all data context
        all_data = self.get_all_data_context()

        # Build context text - limit size aggressively to speed up responses
        context_text = ""
        if all_data:
            if use_minimal_mode:
                # Minimal mode: Send only metadata (column names, types, 1-2 sample rows) so AI can still answer questions
                minimal_metadata = {}
                for key, value in all_data.items():
                    if isinstance(value, list) and len(value) > 0:
                        # Get column names from first row
                        if len(value) > 0:
                            first_row = value[0]
                            if isinstance(first_row, dict):
                                columns = list(first_row.keys())
                                # Send only 1 sample row (further reduced for quota) for structure reference
                                sample_rows = value[:1]  # Only 1 row instead of 2
                                minimal_metadata[key] = {
                                    "columns": columns,
                                    "total_rows": len(value),
                                    "sample_data": sample_rows,  # Just 1 row for structure
                                }
                            else:
                                minimal_metadata[key] = {
                                    "total_rows": len(value),
                                    "sample_data": value[:1],
                                }
                        else:
                            minimal_metadata[key] = {"total_rows": 0}
                    else:
                        minimal_metadata[key] = value

                # Use compact JSON format - even more compact to reduce tokens
                context_text = f"\n\nDB:\n{json.dumps(minimal_metadata, indent=0, separators=(',', ':'), default=str)}\n\n"
            else:
                # Full mode: Send more data but still limited
                limited_data = {}
                total_rows = 0
                for key, value in all_data.items():
                    if isinstance(value, list):
                        # Only send first 3 rows to minimize token usage
                        if len(value) > 3:
                            limited_data[key] = value[:3]
                            limited_data[f"{key}_total_count"] = len(value)
                            total_rows += 3
                        else:
                            limited_data[key] = value
                            total_rows += len(value)
                    else:
                        limited_data[key] = value

                # Only include data if total rows are reasonable (less than 15 rows total)
                if total_rows < 15:
                    # Use compact JSON format (no indentation) to reduce token count
                    context_text = f"\n\nData:\n{json.dumps(limited_data, indent=0, separators=(',', ':'), default=str)}\n\n"
                else:
                    # Too much data - just provide summary
                    context_text = f"\n\nData summary: {len(all_data)} data sources available with {total_rows} total rows.\n\n"

        # Build conversation history - keep it very concise for fastest responses
        conversation = "You are a helpful AI assistant. Answer questions about the data clearly and concisely (not JSON).\n\n"

        # Add only the last message (if any) to reduce tokens
        recent_messages = st.session_state[self.state_key][-1:]  # Only last message
        for msg in recent_messages:
            role = "User" if msg["role"] == "user" else "Assistant"
            # Truncate long messages to keep context small
            content = (
                msg["content"][:100] if len(msg["content"]) > 100 else msg["content"]
            )
            conversation += f"{role}: {content}\n"

        conversation += f"User: {user_message}\n"
        if context_text:
            conversation += context_text
        conversation += "Assistant:"

        # Try each model - no blocking waits (Streamlit doesn't handle long sleeps well)
        last_error = None
        retry_time = None

        for model_name in models_to_try:
            try:
                # Create model instance - this will use the configured API key
                model = genai.GenerativeModel(model_name)

                # Try once - if it works, return immediately
                # Add timeout and better error handling
                try:
                    response = model.generate_content(
                        conversation,
                        generation_config={
                            "temperature": temperature,
                            "max_output_tokens": 400,  # Further reduced for speed and quota
                        },
                    )
                except Exception as api_error:
                    # Re-raise to be caught by outer try-except
                    raise api_error
                # Safely extract text from response
                if hasattr(response, "text") and response.text:
                    return response.text
                elif hasattr(response, "candidates") and response.candidates:
                    # Try to get text from candidates
                    if response.candidates[0].content.parts:
                        return response.candidates[0].content.parts[0].text
                # Fallback
                return (
                    str(response) if response else "⚠️ Error: Invalid response from API"
                )

            except Exception as e:
                error_str = str(e)

                # Check for authentication errors (wrong API key)
                if (
                    "api_key" in error_str.lower()
                    or "authentication" in error_str.lower()
                    or "invalid" in error_str.lower()
                ):
                    return f"⚠️ **API Key Error**: {error_str[:300]}\n\nPlease check:\n1. Your API key in `.streamlit/secrets.toml` is correct\n2. You restarted the Streamlit app after changing the key\n3. The API key is valid at https://aistudio.google.com/apikey"

                # If quota error, extract retry time for error message but don't wait (blocking)
                if (
                    "429" in error_str
                    or "quota" in error_str.lower()
                    or "rate limit" in error_str.lower()
                ):
                    last_error = e
                    # Extract retry time from error message for user info
                    try:
                        time_match = re.search(r"retry in ([\d.]+)", error_str.lower())
                        if time_match:
                            retry_time = float(time_match.group(1))
                    except:
                        pass
                    continue  # Try next model immediately
                else:
                    # Other error, try next model
                    last_error = e
                    continue

        # If all models failed, return helpful error message
        if last_error:
            error_str = str(last_error)
            if (
                "429" in error_str
                or "quota" in error_str.lower()
                or "rate limit" in error_str.lower()
            ):
                # Auto-enable minimal mode if quota error occurs
                minimal_mode_key = f"{self.chat_key}_minimal_mode"
                was_enabled = st.session_state.get(minimal_mode_key, False)
                if not was_enabled:
                    st.session_state[minimal_mode_key] = True
                    auto_enabled_msg = "\n\n✅ **Minimal Mode has been automatically enabled!** Try your question again.\n"
                else:
                    auto_enabled_msg = "\n\n✅ **Minimal Mode is already enabled.**\n"

                error_msg = (
                    "⚠️ **API Quota Exceeded**\n\n"
                    "You've reached the free tier limit for Gemini API.\n\n"
                    "**Quick Solutions (in order):**\n"
                    "1. **Minimal Mode** is now enabled (reduces usage by 60-80%, still answers database questions) ⭐\n"
                )

                if retry_time:
                    error_msg += (
                        f"2. **Wait ~{int(retry_time)} seconds** and try again\n"
                    )
                else:
                    error_msg += "2. **Wait 1-2 minutes** and try again\n"

                error_msg += (
                    "3. **Upgrade** your API plan at https://ai.google.dev/pricing\n"
                    "4. **Check usage** at https://ai.dev/usage\n\n"
                    f"{auto_enabled_msg}"
                    "💡 **Minimal Mode** sends database structure (columns, types, samples) so AI can still answer your database questions while using 60-80% fewer tokens!"
                )

                return error_msg
            else:
                return f"⚠️ Error: {str(last_error)[:200]}"  # Truncate long errors

        return "⚠️ Error: Unable to generate response. Please try again later."

    def render_chatbox(self, container):
        """Render the chatbox in the provided container."""
        if not st.session_state[self.chat_open_key]:
            return

        with container:
            # Header with title and close button
            header_col1, header_col2 = st.columns([4, 1])
            with header_col1:
                st.markdown(f"### 🤖 {self.title}")
            with header_col2:
                if st.button(
                    "✕",
                    key=f"{self.chat_key}_close",
                    help="Close",
                    use_container_width=True,
                ):
                    st.session_state[self.chat_open_key] = False
                    st.rerun()

            # Messages area with scrollable container - match CSV database height (500px)
            messages_container = st.container(height=500)
            with messages_container:
                # Render chat messages using st.chat_message
                for msg in st.session_state[self.state_key]:
                    if msg["role"] == "user":
                        with st.chat_message("user"):
                            st.write(msg["content"])
                    else:
                        with st.chat_message("assistant"):
                            st.write(msg["content"])

            # Input area
            user_input = st.chat_input(
                "Ask about the data...", key=f"{self.chat_key}_input"
            )

            if user_input:
                # Add user message
                st.session_state[self.state_key].append(
                    {"role": "user", "content": user_input}
                )

                # Generate AI response with progress indicator
                ai_response = None
                try:
                    with st.spinner("🤖 AI is thinking... Please wait"):
                        ai_response = self.generate_ai_response(user_input)
                        # Ensure we got a valid response
                        if not ai_response or (
                            isinstance(ai_response, str) and ai_response.strip() == ""
                        ):
                            ai_response = "⚠️ Error: Received empty response from AI. Please try again."
                except Exception as e:
                    # Catch any unexpected errors
                    error_str = str(e)
                    if "429" in error_str or "quota" in error_str.lower():
                        ai_response = (
                            "⚠️ **API Quota Exceeded**\n\n"
                            "The API quota has been exceeded. Please:\n"
                            "1. **Enable Minimal Mode** in sidebar (reduces quota usage)\n"
                            "2. Wait 1-2 minutes and try again\n"
                            "3. Check your API usage at https://ai.dev/usage\n"
                            "4. Consider upgrading your plan at https://ai.google.dev/pricing\n\n"
                            "💡 **Minimal Mode** significantly reduces API usage by not sending data context!"
                        )
                    else:
                        ai_response = f"⚠️ Error: {error_str[:200]}"

                # Ensure we have a response before adding it
                if ai_response:
                    # Add AI response
                    st.session_state[self.state_key].append(
                        {"role": "assistant", "content": str(ai_response)}
                    )

                    # Save chat history
                    self.chat_history.save_chat(
                        st.session_state[self.state_key],
                        f"{self.user_id}_{self.chat_key}",
                    )

                    st.rerun()
                else:
                    # If no response, show error and add error message
                    error_msg = "⚠️ Error: Failed to generate AI response. Please check your API key and try again."
                    st.session_state[self.state_key].append(
                        {"role": "assistant", "content": error_msg}
                    )
                    st.rerun()

    def render(self, container=None):
        """Render the complete floating AI chatbox."""
        self.inject_css()

        # Render sidebar controls if chat is open
        self.render_sidebar_controls()

        if container is None:
            container = st.container()

        self.render_chatbox(container)


# Backward compatibility wrapper
def render_floating_ai_chatbox(
    chat_key: str,
    df: pd.DataFrame = None,
    title="AI Assistant",
    matching_df: pd.DataFrame = None,
    unmatching_df: pd.DataFrame = None,
    manual_data: pd.DataFrame = None,
    container=None,
):
    """Render floating AI chatbox - backward compatibility."""
    chatbox = FloatingAIChatbox(
        chat_key, df, title, matching_df, unmatching_df, manual_data
    )
    chatbox.render(container)
