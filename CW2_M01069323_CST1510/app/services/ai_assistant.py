import streamlit as st
import pandas as pd
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def ai_assistant(title="AI Assistant", context_df=None):
    """Smart AI assistant with table awareness and clean formatting."""

    st.subheader(f"🤖 {title}")

    # -------------------------------
    # CHAT HISTORY
    # -------------------------------
    if "assistant_chat" not in st.session_state:
        st.session_state.assistant_chat = []

    # Show previous messages
    for msg in st.session_state.assistant_chat:
        st.chat_message(msg["role"]).write(msg["content"])

    # -------------------------------
    # USER INPUT
    # -------------------------------
    user_msg = st.chat_input("Ask a question about the data...")
    if not user_msg:
        return

    st.session_state.assistant_chat.append({"role": "user", "content": user_msg})
    st.chat_message("user").write(user_msg)

    # -------------------------------
    # BUILD CONTEXT FOR GEMINI
    # -------------------------------
    ctx = ""

    if isinstance(context_df, pd.DataFrame) and not context_df.empty:
        # Clean DataFrame to avoid dtype/Name: row issues
        ctx_df = context_df.copy()

        # Convert all Series → string cleanly
        ctx += "\n\n### DASHBOARD TABLE SNAPSHOT (first 10 rows)\n"
        ctx += ctx_df.head(10).to_string(index=False)

    full_prompt = (
        f"You are a helpful assistant. Use the table below only if relevant.\n"
        f"{ctx}\n\n"
        f"User question: {user_msg}"
    )

    # -------------------------------
    # AI RESPONSE
    # -------------------------------
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(full_prompt)

        answer = getattr(response, "text", None)
        if not answer:
            answer = response.candidates[0].content.parts[0].text

    except Exception as e:
        answer = f"AI Error: {e}"

    # -------------------------------
    # CLEAN ROW DISPLAY
    # If Gemini tries to output a row in dict/series format → convert to DataFrame
    # -------------------------------
    formatted = answer

    try:
        import ast
        parsed = ast.literal_eval(answer)

        # if parsed is a dict → wrap in DataFrame
        if isinstance(parsed, dict):
            df_clean = pd.DataFrame([parsed])
            st.session_state.assistant_chat.append(
                {"role": "assistant", "content": "Here is the result:"}
            )
            st.chat_message("assistant").dataframe(df_clean)
            return

        # if list of dicts
        if isinstance(parsed, list) and all(isinstance(x, dict) for x in parsed):
            df_clean = pd.DataFrame(parsed)
            st.session_state.assistant_chat.append(
                {"role": "assistant", "content": "Here is the result:"}
            )
            st.chat_message("assistant").dataframe(df_clean)
            return

    except Exception:
        pass  # fallback to plain text

    # -------------------------------
    # NORMAL OUTPUT
    # -------------------------------
    st.session_state.assistant_chat.append({"role": "assistant", "content": formatted})
    st.chat_message("assistant").write(formatted)
