import streamlit as st
import config
from providers import ask_openai, ask_gemini

# Page setup
st.set_page_config(page_title="Multi-LLM Assistant", page_icon="🤖", layout="centered")
st.title("🤖 Multi-LLM Chatbot")

# Display current settings in the sidebar
st.sidebar.title("Configuration")
st.sidebar.write(f"**Provider:** `{config.PROVIDER}`")
active_model = config.OPENAI_MODEL if config.PROVIDER == "openai" else config.GEMINI_MODEL
st.sidebar.write(f"**Model:** `{active_model}`")

# Store conversation history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User chat input
if prompt := st.chat_input("Type your message here..."):
    # Render user prompt
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate model response
    with st.chat_message("assistant"):
        with st.spinner("Generating answer..."):
            try:
                if config.PROVIDER == "openai":
                    response = ask_openai(prompt)
                elif config.PROVIDER == "gemini":
                    response = ask_gemini(prompt)
                else:
                    response = "Ollama requires a local GPU server and is not available on cloud hosting."
                
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as err:
                st.error(f"Error communicating with provider: {err}")