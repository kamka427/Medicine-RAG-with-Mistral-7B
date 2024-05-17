import streamlit as st
from rag import index


st.set_page_config(page_title="Chat about medicine with Mistral 7B", page_icon="🦙", layout="centered", initial_sidebar_state="auto", menu_items=None)
st.title("Chat about medicine with Mistral 7B 💬🦙")

if "messages" not in st.session_state.keys():
    st.session_state.messages = [
         {"role": "system", "content": "You are a doctor and you are chatting with a patient. Try to diagnose the patient's symptoms and recommend a medicine. They can also ask you questions about any medicine. Act as a healthcare professional. Try to diagnose the patient."},
        {"role": "assistant", "content": "Hello! I am Mistral 7B, a medical assistant. How can I help you today?"}
    ]

if "chat_engine" not in st.session_state.keys():
        st.session_state.chat_engine = index.as_chat_engine(chat_mode="context", verbose=True)

if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)
