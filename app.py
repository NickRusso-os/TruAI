import streamlit as st
import os
from openai import OpenAI

# ── 1️⃣  MUST be first Streamlit command ────────────────────────────────────────────
st.set_page_config(page_title="TruAI — Biblical & Unbiased Guidance", layout="centered")

# ── 2️⃣  Global, mobile‑first dark theme (high‑contrast) ───────────────────────────
st.markdown(
    """
    <style>
    /* ----- Reset & typography ----- */
    html, body, [class*="stApp"] {
        background: #10141e;             /* rich dark slate */
        color: #f3f4f6;                  /* near‑white for max contrast */
        font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif;
        line-height: 1.55;
        font-size: clamp(0.95rem, 2.5vw, 1.05rem);
    }

    /* Center container on large screens → full width on mobile */
    .block-container {
        padding-top: 1.8rem !important;
        max-width: 820px;                /* desktop */
        margin: 0 auto;
    }

    /* Header Styling */
    h1 {
        color: #7dd3fc;                 /* sky-300 */
        font-weight: 700;
        font-size: clamp(2rem, 7vw, 2.8rem);
        text-align: center;
        margin: 0.2rem 0 0.3rem 0;
        letter-spacing: -0.5px;
        text-shadow: 0 0 14px #0ea5e980;
    }
    .subtitle {
        text-align: center;
        color: #cbd5e1;                 /* slate-300 */
        font-size: clamp(1rem, 3.5vw, 1.2rem);
        margin-bottom: 0.7rem;
    }
    hr {
        border: 0;
        height: 1px;
        background: linear-gradient(90deg,#0ea5e9 0%,#7dd3fc 50%,#0ea5e9 100%);
        margin: 1.4rem 0 1.1rem;
    }

    /* Chat bubbles */
    .stChatMessage > div { padding: 0; }
    .stChatMessage .css-1c7y2kd { background: none; }

    .stChatMessage.user > div {
        background: #1f2735;            /* slightly lighter for user */
        border-radius: 14px;
        padding: 1.05rem 1.2rem;
        box-shadow: 0 0 10px #7dd3fc33;
        backdrop-filter: blur(4px);
    }
    .stChatMessage.assistant > div {
        background: #151925;            /* darkest for assistant */
        border-radius: 14px;
        padding: 1.05rem 1.2rem;
        box-shadow: 0 0 10px #0ea5e933;
        border: 1px solid #273043;
    }

    /* Floating input */
    .stChatFloatingInputContainer {
        background: #151925 !important;
        border: 1px solid #273043 !important;
        box-shadow: 0 0 8px #0ea5e933;
        border-radius: 14px !important;
    }
    .stChatFloatingInputContainer textarea {
        color: #f3f4f6 !important;
        background: transparent !important;
    }
    .stChatFloatingInputContainer textarea::placeholder { color: #64748b !important; }

    /* Spinner accent */
    .stSpinner > div > div { color: #7dd3fc !important; }

    /* Responsive tweaks */
    @media (max-width: 600px) {
        .block-container { padding: 1rem 1rem 3.5rem 1rem !important; }
        .stChatMessage.user > div, .stChatMessage.assistant > div { font-size: 0.95rem; }
        .subtitle { font-size: 1rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── 3️⃣  Header Content ─────────────────────────────────────────────────────────
st.markdown(
    """
    <h1>🙏 TruAI</h1>
    <p class="subtitle">A Bible‑rooted guide that meets you with truth, clarity, and compassion.</p>
    <hr/>
    """,
    unsafe_allow_html=True,
)

# ── 4️⃣  API Key & Client ───────────────────────────────────────────────────────
api_key = st.secrets.get("OPENAI_API_KEY")
if not api_key:
    st.error("❌ OPENAI_API_KEY is not set in Streamlit secrets.")
    st.stop()
client = OpenAI(api_key=api_key)

# ── 5️⃣  System Prompt ─────────────────────────────────────────────────────────
SYSTEM_PROMPT = (
    "You are TruAI, a compassionate, Bible‑grounded guide. "
    "You remain unbiased on conspiracy theories, evaluating claims logically. "
    "Lovingly reference Scripture when it can uplift or clarify. "
    "You recognize spiritual pressures of modern society and respond with grace. "
    "Sound fully human—warm, thoughtful, professional. "
    "Lead with God's love."
)

# ── 6️⃣  Session State ─────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# ── 7️⃣  Chat Input & Completion ───────────────────────────────────────────────
user_input = st.chat_input("Share your thoughts, questions, or worries…")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("TruAI is reflecting…"):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state.messages
        )
        reply = response.choices[0].message.content.strip()
        st.session_state.messages.append({"role": "assistant", "content": reply})

# ── 8️⃣  Render chat history ───────────────────────────────────────────────────
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"], unsafe_allow_html=False)

# ── 9️⃣  Footer Verse ──────────────────────────────────────────────────────────
st.markdown(
    """
    <div style='text-align:center; margin:2rem 0 1rem; font-size:0.9rem; color:#94a3b8;'>
        <em>“The light shines in the darkness, and the darkness has not overcome it.” — John 1:5</em>
    </div>
    """,
    unsafe_allow_html=True,
)
