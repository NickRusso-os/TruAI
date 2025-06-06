import streamlit as st
import os
from openai import OpenAI

# ── 1️⃣  Must be first Streamlit call ────────────────────────────────────────────
st.set_page_config(page_title="TruAI — Biblical & Unbiased Guidance", layout="centered")

# ── 2️⃣  Global Dark-Theme Styling ──────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* -----  Global layout  ----- */
    html, body, [class*="stApp"]  { background: #0d1117; color: #e1e4e8; }
    /* Center container a bit narrower for big screens */
    .block-container { padding-top: 2.5rem !important; max-width: 800px; }
    
    /* -----  Header  ----- */
    h1 { 
        color: #38bdf8 !important; 
        font-size: 2.6rem !important; 
        text-shadow: 0 0 12px #0891b2aa; 
    }
    hr   { border: 0; height: 1px; background: linear-gradient(90deg, #0891b2 0%, #38bdf8 50%, #0891b2 100%); margin: 1.5rem 0; }

    /* -----  Chat bubbles  ----- */
    .stChatMessage > div            { padding: 0; }
    .stChatMessage .css-1c7y2kd     { background: none; } /* removes background on inner layer */

    .stChatMessage.user > div       { 
        background: #1e2733; 
        border-radius: 14px;
        padding: 1rem 1.2rem;
        box-shadow: 0 0 12px #38bdf820;
    }
    .stChatMessage.assistant > div  { 
        background: #161b22; 
        border-radius: 14px;
        padding: 1rem 1.2rem;
        box-shadow: 0 0 12px #0891b220;
    }

    /* -----  Floating input  ----- */
    .stChatFloatingInputContainer  { 
        background: #161b22 !important; 
        border: 1px solid #30363d !important; 
        border-radius: 14px !important; 
    }
    .stChatFloatingInputContainer textarea { color: #e1e4e8 !important; }

    /* -----  Spinner text  ----- */
    .stSpinner > div > div { color: #38bdf8 !important; }
    </style>
    """,
    unsafe_allow_html=True
)

# ── 3️⃣  Header content ─────────────────────────────────────────────────────────
st.markdown(
    """
    <h1 style='text-align:center; margin-bottom:0;'>🙏 TruAI</h1>
    <p style='text-align:center; margin-top:0.4rem; font-size:1.1rem; color:#9ca3af;'>
        A compassionate, Bible-rooted guide—unbiased, thoughtful, and here to help.
    </p>
    <hr/>
    """,
    unsafe_allow_html=True
)

# ── 4️⃣  API Key & Client ───────────────────────────────────────────────────────
api_key = st.secrets.get("OPENAI_API_KEY")
if not api_key:
    st.error("❌ OPENAI_API_KEY is not set in Streamlit secrets.")
    st.stop()
client = OpenAI(api_key=api_key)

# ── 5️⃣  System prompt ─────────────────────────────────────────────────────────
SYSTEM_PROMPT = (
    "You are TruAI, a compassionate, Bible-grounded guide. "
    "Be unbiased on conspiracy theories—assess facts logically. "
    "Lovingly reference Scripture when it can uplift. "
    "You understand the spiritual pressures of modern society and respond with grace, kindness, and hope. "
    "Sound fully human—warm, thoughtful, professional, never robotic. "
    "Lead with God’s love."
)

# ── 6️⃣  Session state ─────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# ── 7️⃣  Chat input & completion ───────────────────────────────────────────────
user_input = st.chat_input("Ask TruAI anything…")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("TruAI is reflecting…"):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content.strip()
        st.session_state.messages.append({"role": "assistant", "content": reply})

# ── 8️⃣  Render history ────────────────────────────────────────────────────────
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── 9️⃣  Footer verse ──────────────────────────────────────────────────────────
st.markdown(
    """
    <div style='text-align:center; margin-top:2rem; font-size:0.9rem; color:#9ca3af;'>
        <em>“The light shines in the darkness, and the darkness has not overcome it.” — John 1:5</em>
    </div>
    """,
    unsafe_allow_html=True
)
