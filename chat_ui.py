import streamlit as st
from models.llm_model import FamilyLLM
from openai import OpenAI

# Set OpenAI key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Family AI Assistant", page_icon="🧑‍🤝‍🧑")
st.title("🤖 Family Career Coach")
st.caption("Ask about your family members' careers, advice, and growth paths!")

# Initialize conversation
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant and career strategist."}
    ]

# Load family data
family_llm = FamilyLLM()
intro = "Here is my family:\n" + family_llm.get_family_list()

# Inject initial message on first load
if "initialized" not in st.session_state:
    st.session_state.messages.append({"role": "user", "content": intro})
    st.session_state.initialized = True

# Chat input
user_input = st.chat_input("Ask me about your family...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Thinking..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=st.session_state.messages,
                max_tokens=1000,
                temperature=0.7
            )
            reply = response.choices[0].message.content.strip()
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            reply = f"Error: {e}"
            st.session_state.messages.append({"role": "assistant", "content": reply})

# Display full chat
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("🧑"):
            st.markdown(msg["content"])
    elif msg["role"] == "assistant":
        with st.chat_message("🤖"):
            st.markdown(msg["content"])

# Reset chat button
if st.button("🔁 Reset Chat"):
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant and career strategist."},
        {"role": "user", "content": intro}
    ]
    st.success("Chat history reset!")
