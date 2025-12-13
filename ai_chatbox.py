import streamlit as st
import pandas as pd

from app.services.ai_assistant import ai_assistant_response


class AIChatbox:
    """AI Chatbox component for interactive AI conversations."""

    def __init__(
        self, chat_key: str, df: pd.DataFrame, title="🤖 AI Assistant", height=500
    ):
        """Initialize AIChatbox component."""
        self.chat_key = chat_key
        self.df = df
        self.title = title
        self.height = height
        self.state_key = f"{chat_key}_chat_history"

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
        """Handle user input and generate AI response."""
        user_input = st.text_input("Ask about the data", key=f"{self.chat_key}_input")

        if user_input:
            st.session_state[self.state_key].append(
                {"role": "user", "content": user_input}
            )

            reply = ai_assistant_response(user_input, self.df)

            st.session_state[self.state_key].append(
                {"role": "assistant", "content": reply}
            )

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
