import streamlit as st
import openai

st.set_page_config(page_title="Custom GPT Chatbot", layout="centered")

st.title("💬 Custom GPT Chatbot")
st.caption("Ask anything. It's tuned to your personality or purpose.")

openai.api_key = st.secrets["OPENAI_API_KEY"]

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful and sarcastic chatbot."}]

user_input = st.chat_input("Ask something...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Thinking..."):
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=st.session_state.messages
        )
        reply = response["choices"][0]["message"]["content"]
        st.session_state.messages.append({"role": "assistant", "content": reply})

for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
