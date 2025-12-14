"""
AI Chatbox Component Module
Provides interactive AI chat interface with message history and user input handling.
"""

import streamlit as st
import pandas as pd

# AI response generation service
from app.services.ai_assistant import ai_assistant_response


class AIChatbox:
    """
    AI Chatbox component for interactive AI conversations.
    Manages chat history, displays messages, and handles user input.
    """

    def __init__(
        self, chat_key: str, df: pd.DataFrame, title="🤖 AI Assistant", height=500
    ):
        """
        Initialize AIChatbox component with unique key and data context.
        
        Args:
            chat_key: Unique identifier for this chat instance
            df: DataFrame containing data context for AI responses
            title: Display title for the chatbox
            height: Height of the chatbox in pixels
        """
        self.chat_key = chat_key
        self.df = df  # Data context for AI responses
        self.title = title
        self.height = height
        # Create unique session state key for chat history
        self.state_key = f"{chat_key}_chat_history"

        # Initialize empty chat history if not exists
        if self.state_key not in st.session_state:
            st.session_state[self.state_key] = []

    def render_header(self):
        """Render chatbox header."""
        st.markdown(
            f"""
        <div style="
            background: rgba(20,0,30,0.6);
            border-radius: 16px;
            padding: 15px;
            box-shadow: 0 0 18px rgba(255,0,255,0.4);
            height: {self.height}px;
            display: flex;
            flex-direction: column;
        ">
        <h3 style="text-align:center; color:#ff33ff;">{self.title}</h3>
        """,
            unsafe_allow_html=True,
        )

    def render_messages(self):
        """Render chat messages."""
        for msg in st.session_state[self.state_key]:
            align = "right" if msg["role"] == "user" else "left"
            bg = (
                "rgba(255,0,255,0.2)"
                if msg["role"] == "user"
                else "rgba(0,255,204,0.2)"
            )

            st.markdown(
                f"""
            <div style="
                background:{bg};
                padding:10px;
                border-radius:10px;
                margin-bottom:8px;
                text-align:{align};
            ">
            {msg["content"]}
            </div>
            """,
                unsafe_allow_html=True,
            )

    def handle_user_input(self):
        """
        Handle user input, generate AI response, and update chat history.
        Processes user messages and triggers AI response generation.
        """
        # Get user input from text input field
        user_input = st.text_input("Ask about the data", key=f"{self.chat_key}_input")

        # Process input if user submitted a message
        if user_input:
            # Add user message to chat history
            st.session_state[self.state_key].append(
                {"role": "user", "content": user_input}
            )

            # Generate AI response using data context
            reply = ai_assistant_response(user_input, self.df)

            # Add AI response to chat history
            st.session_state[self.state_key].append(
                {"role": "assistant", "content": reply}
            )

            # Rerun app to display new messages
            st.rerun()

    def render(self):
        """Render the complete AI chatbox."""
        self.render_header()
        self.render_messages()
        self.handle_user_input()
        st.markdown("</div>", unsafe_allow_html=True)


# Backward compatibility wrapper function
def render_ai_chatbox(
    chat_key: str, df: pd.DataFrame, title="🤖 AI Assistant", height=500
):
    """Render AI chatbox - backward compatibility."""
    chatbox = AIChatbox(chat_key, df, title, height)
    chatbox.render()
