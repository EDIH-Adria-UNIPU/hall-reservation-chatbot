import streamlit as st
from openai import OpenAI

print(st.secrets["OPENAI_API_KEY"])

st.title("IDA - chatbot za rezevaciju dvorana")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not st.secrets["OPENAI_API_KEY"]:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=st.session_state.messages
    )
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)