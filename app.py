import streamlit as st
import os
from openai import OpenAI

# ── 1️⃣  First Streamlit call ───────────────────────────────────────────────────
st.set_page_config(page_title="TruAI — Biblical & Unbiased Guidance", layout="centered")

# ── 2️⃣  Global Apple‑inspired Light Theme ──────────────────────────────────────
st.markdown(
    """
    <style>
    /* ---- Base & typography ---- */
    html, body, [class*='stApp'] {
        background: #fdfdfd;              /* pristine white */
        color: #1c1c1e;                   /* near‑black text */
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        line-height: 1.58;
        font-size: clamp(0.96rem, 2.3vw, 1.05rem);
    }
    .block-container { padding: 2rem 1rem 4rem 1rem; max-width: 820px; margin: 0 auto; }

    /* ---- Links ---- */
    a {
        color: #0a84ff;                   /* iOS blue for links */
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }

    /* ---- Subtle glow background behind main container ---- */
    .block-container:before {
        content: "";
        position: fixed;
        top: 50%;
        left: 50%;
        width: 1200px;
        height: 1200px;
        transform: translate(-50%, -50%);
        background: radial-gradient(circle at center, #a5d8ff33 0%, #c1f0ff11 40%, transparent 70%);
        filter: blur(120px);
        z-index: -1;
    }

    /* ---- Header ---- */
    h1 {
        color: #0a84ff;                   /* iOS blue */
        font-size: clamp(2.2rem, 6vw, 2.8rem);
        font-weight: 700;
        text-align: center;
        margin: 0.3rem 0 0.4rem;
    }
    .subtitle {
        text-align: center;
        color: #515154;
        font-size: clamp(1.05rem, 2.8vw, 1.25rem);
        margin-bottom: 0.9rem;
    }
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg,#0a84ff 0%,#64d2ff 50%,#0a84ff 100%);
        margin: 1.2rem 0 1.2rem;
    }

    /* ---- Chat cards ---- */
    .stChatMessage > div { padding: 0; }
    .stChatMessage .css-1c7y2kd { background: none; }

    .stChatMessage.user > div {
        background: rgba(0,0,0,0.04);
        border-radius: 16px;
        padding: 1.05rem 1.2rem;
        backdrop-filter: blur(12px);
        box-shadow: 0 2px 6px #00000014, 0 1px 3px #0000000d;
    }
    .stChatMessage.assistant > div {
        background: rgba(255,255,255,0.6);
        border: 1px solid #e5e5ea;
        border-radius: 16px;
        padding: 1.05rem 1.2rem;
        backdrop-filter: blur(24px) saturate(180%);
        box-shadow: 0 2px 10px #0000001a, 0 1px 4px #0000000f;
        color: #1c1c1e; /* Ensure text is dark for assistant messages */
    }

    /* ---- Floating input ---- */
    .stChatFloatingInputContainer {
        background: rgba(255,255,255,0.8) !important;
        border: 1px solid #d1d1d6 !important;
        backdrop-filter: blur(24px) saturate(180%);
        border-radius: 16px !important;
        box-shadow: 0 2px 10px #0000001a;
    }
    .stChatFloatingInputContainer textarea {
        color: #1c1c1e !important;
        background: transparent !important;
    }
    .stChatFloatingInputContainer textarea::placeholder { color: #8e8e93 !important; }

    /* ---- Spinner accent ---- */
    .stSpinner > div > div { color: #0a84ff !important; }

    /* ---- Mobile tweaks ---- */
    @media(max-width:600px){
        .block-container { padding: 1.2rem 1rem 4.5rem 1rem !important; }
        .stChatMessage.user > div, .stChatMessage.assistant > div { font-size: 0.95rem; }
        .subtitle { font-size: 1.05rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── 3️⃣  Header ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <h1>🙏 TruAI</h1>
    <p class='subtitle'>A Bible‑rooted guide that meets you with truth, clarity, and compassion.</p>
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
    "You are TruAI, a compassionate, Bible-grounded guide. "
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
    <div style='text-align:center; margin:2.5rem 0 1.5rem; font-size:0.9rem; color:#6e6e73;'>
        <em>“The light shines in the darkness, and the darkness has not overcome it.” — John 1:5</em>
    </div>
    """,
    unsafe_allow_html=True,
)
