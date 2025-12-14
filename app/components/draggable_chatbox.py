"""
Draggable Chatbox Component Module
Chat window positioned next to database section with scrollable history and inline input.
Simple, reliable implementation with input inside chatbox for better UX.
"""

import streamlit as st
import pandas as pd
import re
import html
# Import AI response generation function
from app.components.simple_ai_chat import generate_response


def draggable_chatbox(
    title="AI Assistant", context_df=None, role_hint=None, unmatching_df=None
):
    """
    Chatbox positioned next to database section.
    Has scrollable chat history, input inside chatbox, and matches database height.

    Args:
        title: Title for the chatbox
        context_df: Main combined DataFrame (database + matching + manual)
        role_hint: Hint about the data type (cyber_incident, it_ticket, dataset)
        unmatching_df: Unmatching uploaded data (separate DataFrame)
    """

    # Initialize chat history with unique key based on role hint
    chat_key = f"draggable_chat_{role_hint or 'default'}"
    if chat_key not in st.session_state:
        st.session_state[chat_key] = []

    # Add welcome message if chat history is empty (first time opening)
    if len(st.session_state[chat_key]) == 0:
        welcome_msg = "Hello! I'm your AI assistant. I can help you analyze your data, answer questions, and provide insights. Try asking me about your data!"
        st.session_state[chat_key].append({"role": "assistant", "content": welcome_msg})

    # CSS Styling for chatbox
    st.markdown(
        """
    <style>
    .chatbox-wrapper {
        background: #ffffff;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        border: 1px solid #e0e0e0;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        height: 500px;
    }
    
    .chatbox-header {
        background: linear-gradient(135deg, #7b2ff7, #a855f7);
        padding: 14px 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-shrink: 0;
    }
    
    .chatbox-title {
        color: white;
        font-size: 16px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .chatbox-controls {
        display: flex;
        gap: 8px;
    }
    
    .chatbox-control-btn {
        background: rgba(255, 255, 255, 0.2);
        border: none;
        color: white;
        width: 28px;
        height: 28px;
        border-radius: 6px;
        cursor: pointer;
        font-size: 16px;
    }
    
    .chatbox-messages {
        flex: 1;
        overflow-y: auto;
        overflow-x: hidden;
        padding: 16px;
        background: #f5f5f5;
        display: flex;
        flex-direction: column;
        gap: 12px;
        min-height: 0;
    }
    
    .chatbox-message {
        display: flex;
        align-items: flex-start;
        gap: 8px;
        max-width: 85%;
    }
    
    .chatbox-message.user {
        align-self: flex-end;
        margin-left: auto;
        flex-direction: row-reverse;
    }
    
    .chatbox-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        flex-shrink: 0;
    }
    
    .chatbox-avatar.user {
        background: linear-gradient(135deg, #3b82f6, #06b6d4);
        color: white;
    }
    
    .chatbox-avatar.bot {
        background: linear-gradient(135deg, #8b5cf6, #a855f7);
        color: white;
    }
    
    .chatbox-bubble {
        padding: 10px 14px;
        border-radius: 18px;
        word-wrap: break-word;
        font-size: 14px;
        line-height: 1.4;
        color: #333;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    }
    
    .chatbox-bubble.user {
        background: linear-gradient(135deg, #3b82f6, #06b6d4);
        color: white;
    }
    
    .chatbox-bubble.bot {
        background: #ffffff;
        color: #333;
        border: 1px solid #e0e0e0;
    }
    
    .chatbox-messages::-webkit-scrollbar {
        width: 10px;
    }
    
    .chatbox-messages::-webkit-scrollbar-track {
        background: #e0e0e0;
        border-radius: 5px;
    }
    
    .chatbox-messages::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 5px;
    }
    
    .chatbox-messages {
        scrollbar-width: thin;
        scrollbar-color: #888 #e0e0e0;
    }
    
    .chatbox-input-container {
        background: linear-gradient(135deg, #e0d5f5, #f3e8ff);
        padding: 12px 16px;
        border-top: 1px solid #e0e0e0;
        flex-shrink: 0;
    }
    
    /* Style Streamlit chat input to look like our custom input */
    .chatbox-input-container div[data-testid="stChatInput"] {
        background: white;
        border-radius: 20px;
        border: 1px solid #d0c4e8;
    }
    
    .chatbox-input-container div[data-testid="stChatInput"]:focus-within {
        border-color: #7b2ff7;
        box-shadow: 0 0 0 2px rgba(123, 47, 247, 0.1);
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Build chat messages HTML
    messages_html = '<div class="chatbox-messages">'
    for msg in st.session_state[chat_key]:
        is_user = msg["role"] == "user"
        message_class = "user" if is_user else "bot"
        avatar_class = "user" if is_user else "bot"
        bubble_class = "user" if is_user else "bot"

        # Format content
        content = str(msg["content"])
        content = re.sub(r"\*\*([^*]+?)\*\*", r"<strong>\1</strong>", content)
        content = content.replace("\n", "<br>")
        parts = re.split(r"(<strong>.*?</strong>|<br>)", content, flags=re.DOTALL)
        escaped_parts = []
        for part in parts:
            if (
                part.startswith("<strong>")
                or part == "<br>"
                or part.startswith("</strong>")
            ):
                escaped_parts.append(part)
            elif part:
                escaped_parts.append(html.escape(part))
        content = "".join(escaped_parts)

        avatar_icon = "👤" if is_user else "🤖"

        messages_html += f'<div class="chatbox-message {message_class}">'
        messages_html += (
            f'<div class="chatbox-avatar {avatar_class}">{avatar_icon}</div>'
        )
        messages_html += f'<div class="chatbox-bubble {bubble_class}">{content}</div>'
        messages_html += "</div>"
    messages_html += "</div>"

    # Build chatbox HTML
    chatbox_html = '<div class="chatbox-wrapper">'
    chatbox_html += '<div class="chatbox-header">'
    chatbox_html += '<div class="chatbox-title">'
    chatbox_html += "<span>🤖</span>"
    chatbox_html += f"<span>{html.escape(title)}</span>"
    chatbox_html += "</div>"
    chatbox_html += '<div class="chatbox-controls">'
    chatbox_html += '<button class="chatbox-control-btn">−</button>'
    chatbox_html += '<button class="chatbox-control-btn">×</button>'
    chatbox_html += "</div>"
    chatbox_html += "</div>"
    chatbox_html += messages_html
    chatbox_html += "</div>"

    # Display chatbox
    st.markdown(chatbox_html, unsafe_allow_html=True)

    # Input area - use Streamlit's native chat_input inside a styled container
    with st.container():
        st.markdown('<div class="chatbox-input-container">', unsafe_allow_html=True)
        user_input = st.chat_input(
            "Type your message here...", key=f"draggable_input_{role_hint}"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # Auto-scroll JavaScript
    st.markdown(
        """
    <script>
    (function() {
        function scrollToBottom() {
            const messagesDiv = document.querySelector('.chatbox-messages');
            if (messagesDiv) {
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            }
        }
        setTimeout(scrollToBottom, 100);
        const observer = new MutationObserver(scrollToBottom);
        const messagesDiv = document.querySelector('.chatbox-messages');
        if (messagesDiv) {
            observer.observe(messagesDiv, { childList: true, subtree: true });
        }
    })();
    </script>
    """,
        unsafe_allow_html=True,
    )

    # Handle user input when message is submitted
    if user_input:
        # Add user message to chat history
        st.session_state[chat_key].append({"role": "user", "content": user_input})
        # Generate AI response using context data and role hint
        ai_response = generate_response(
            user_input, context_df, role_hint, unmatching_df
        )
        # Add AI response to chat history
        st.session_state[chat_key].append({"role": "assistant", "content": ai_response})
        # Rerun to display new messages
        st.rerun()

    # Clear chat button - resets chat history
    if st.button(
        "🗑️ Clear Chat", key=f"clear_btn_{role_hint}", use_container_width=True
    ):
        # Clear all messages from chat history
        st.session_state[chat_key] = []
        st.rerun()
