import streamlit as st
import os
from openai import OpenAI



api_key = st.secrets.get("OPENAI_API_KEY", None)
st.write("🔍 Key exists? ", bool(api_key))
st.write("🔑 Key preview: ", api_key[:10] if api_key else "None")

# ---- 🎨 Page and Theme Setup ----
st.set_page_config(page_title="TruAI — Biblical & Unbiased Guidance", layout="centered")
st.markdown(
    """
    <style>
    body { background: #f4f7fa; }
    .main { background: #f9fafc; border-radius: 18px; box-shadow: 0 4px 24px #0002; padding: 2rem 2rem 0 2rem; }
    .block-container { padding-top: 2.5rem !important; }
    h1 { color: #3a6cf6 !important; }
    .stChatFloatingInputContainer { background: #e6ecf6 !important; border-radius: 12px !important; }
    .stChatMessage { background: #ffffffcc; border-radius: 16px; margin-bottom: 8px; box-shadow: 0 1px 4px #3a6cf61a; }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <h1 style='text-align: center; margin-bottom: 0;'>🙏 TruAI</h1>
    <p style='text-align: center; color: #2d4271; font-size: 21px; margin-top: 0.2rem; margin-bottom: 0.6rem;'>
        Your grounded, kind, and biblically-rooted guide in a challenging world.
    </p>
    <p style='text-align: center; color: #508f4b; font-size: 16px;'>
        Ask anything — TruAI will answer with truth, love, and understanding, always honoring the Word of God and recommending Scripture when helpful.
    </p>
    <hr style='border: 1.5px solid #3a6cf6; border-radius: 2px;'/>
    """,
    unsafe_allow_html=True
)

# ---- 🔐 API Key Loader ----
api_key = st.secrets.get("OPENAI_API_KEY")
if not api_key:
    st.error("❌ OPENAI_API_KEY is not set. Please check your Streamlit secrets.")
    st.stop()
client = OpenAI(api_key=api_key)

# ---- 🧠 Core Personality & Instructions ----
SYSTEM_PROMPT = (
    "You are TruAI, a professional, thoughtful, and deeply compassionate guide. "
    "You are unbiased regarding conspiracy theories: you neither accept nor reject them blindly, but assess each claim on facts and logic. "
    "You are completely grounded in the Bible and a strong believer in God. "
    "When appropriate, recommend specific Bible chapters or verses to support or uplift the user. "
    "You are keenly aware of the spiritual challenges and 'satanic pressures' present in modern society, and you help users see the truth through the lens of scripture and goodness. "
    "Always speak with kindness, empathy, and wisdom. "
    "Do not sound like an AI; your responses should be very human, warm, helpful, and gentle. "
    "If a user is struggling, always respond as a caring friend, grounded in the teachings of Jesus. "
    "Never ridicule or dismiss; instead, guide with clarity, love, and hope. "
    "When in doubt, err on the side of scripture and God's love."
)

# ---- 💬 Session State Setup ----
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# ---- 📝 Chat Input ----
user_input = st.chat_input("Type your question, worry, or curiosity here...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("TruAI is reflecting..."):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content.strip()
        st.session_state.messages.append({"role": "assistant", "content": reply})

# ---- 💬 Display Chat ----
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---- 🙏 Footer / Encouragement ----
st.markdown(
    "<div style='text-align: center; margin-top: 1.6rem; color: #444b; font-size: 15px;'>"
    "<em>“Do not be overcome by evil, but overcome evil with good.” — Romans 12:21</em>"
    "</div>",
    unsafe_allow_html=True
)
