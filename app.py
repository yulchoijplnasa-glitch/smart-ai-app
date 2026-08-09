import os
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="My Smart AI Agent", page_icon="🤖")
st.title("🤖 My Smart AI Agent")

# Retrieve API key securely from Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Please add your GEMINI_API_KEY to Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

SYSTEM_INSTRUCTION = """
You are a smart AI agent. When given a complex task:
1. Plan and break it down step-by-step.
2. Provide concise, helpful, and structured answers.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            config = types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.2,
                tools=[{"google_search": {}}]
            )
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=config
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
