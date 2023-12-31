import streamlit as st
from openai import OpenAI


st.set_page_config(page_title="Chatbot", page_icon="🤖", layout="centered", initial_sidebar_state="auto", menu_items=None)

client = OpenAI(api_key=st.secrets["api_key"])

if 'messages' in st.session_state:
    messages = st.session_state['messages']
else:
    messages = [{"role": "system", "content": "You are a helpful assistant."}]

def all_messages():
    for message in messages:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.write("User : ", message["content"])
        elif message["role"] == "assistant":
            with st.chat_message("assistant"):
                st.write("Ai : ", message["content"])

all_messages()
prompt = st.chat_input("Say something")
if prompt:
    with st.spinner('Wait for it...'):
        messages.append({"role": "user", "content": prompt})
        response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages
                    )
        messages.append({"role": "assistant", "content": response.choices[0].message.content})
        st.session_state['messages'] = messages
    st.experimental_rerun()






