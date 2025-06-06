import streamlit as st
import os
from openai import OpenAI

# Page setup
st.set_page_config(page_title="🤖 TruAI - Custom Chatbot", layout="centered")
st.markdown(
    """
    <h1 style='text-align: center; color: #4A90E2;'>🤖 TruAI</h1>
    <p style='text-align: center; font-size: 18px;'>Your custom-tuned AI assistant. Ask anything.</p>
    <hr style='border: 1px solid #4A90E2;'/>
    """,
    unsafe_allow_html=True
)

# Load API key
# Load API key from Streamlit secrets (Streamlit Cloud will inject this)
api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

if not api_key:
    st.error("❌ OPENAI_API_KEY is not set. Please check your Streamlit secrets.")
    st.stop()

client = OpenAI(api_key=api_key)


# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful, sarcastic assistant named TruAI."}
    ]

# Chat input
user_input = st.chat_input("Ask TruAI anything...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("TruAI is thinking..."):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})

# Display chat history
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
