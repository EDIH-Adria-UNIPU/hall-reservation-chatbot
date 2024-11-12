import streamlit as st
from openai import OpenAI
import os
from datetime import datetime

from utils import prepare_prompt

st.title("IDA - chatbot za rezevaciju dvorana")

# Add initial system and assistant messages
if "messages" not in st.session_state:
    st.session_state.messages = []

    # Get current date and time
    current_datetime = datetime.now()
    current_date = current_datetime.strftime("%Y-%m-%d")
    current_time = current_datetime.strftime("%H:%M")

    system_message = prepare_prompt(
        os.path.join("src", "prompts", "system_message.txt"),
        date=current_date,
        time=current_time,
    )
    st.session_state.messages.append({"role": "system", "content": system_message})

    st.session_state.messages.append(
        {"role": "assistant", "content": "Pozdrav! Ja sam asistent za rezervacije u Coworking Pula. Mogu vam pomoći rezervirati dvoranu, sobu za sastanke ili coworking prostor. Koji prostor vas zanima?"}
    )

for msg in st.session_state.messages:
    if msg["role"] != "system":  # Only display non-system messages
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
