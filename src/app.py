import streamlit as st
from openai import OpenAI
import os
import json
from datetime import datetime

from utils import prepare_prompt, get_available_tools
from data_manager import DataManager

st.title("IDA - chatbot za rezevaciju dvorana")

manager = DataManager()
tools = get_available_tools()

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
        {
            "role": "assistant",
            "content": "Pozdrav! Ja sam asistent za rezervacije u Coworking Pula. Mogu vam pomoći rezervirati dvoranu, sobu za sastanke ili coworking prostor. Koji prostor vas zanima?",
        }
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
        model="gpt-4o-mini", messages=st.session_state.messages, tools=tools
    )

    if response.choices[0].message.content is not None:
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
    elif response.choices[0].message.tool_calls:
        # TODO: another function for making reservations (the conversation should end after this function
        # and the subsequent response from the assistant)

        print("\nFunction call detected:", response.choices[0].message)
        tool_call = response.choices[0].message.tool_calls[0]
        arguments = json.loads(tool_call.function.arguments)
        print("\nFunction call with arguments:", arguments)
        date = arguments.get("date")
        start_hour = arguments.get("start_hour")
        end_hour = arguments.get("end_hour")

        result = manager.check_availability(date, start_hour, end_hour)

        print("\nAvailable slots:", result)

        # Add message with tool call
        st.session_state.messages.append(response.choices[0].message)

        # Add message with tool output
        st.session_state.messages.append(
            {
                "role": "tool",
                "content": str(result),
                "tool_call_id": tool_call.id,
            }
        )

        # Make another call to OpenAI API to continue the conversation
        response = client.chat.completions.create(
            model="gpt-4o-mini", messages=st.session_state.messages, tools=tools
        )

        if response.choices[0].message.content is not None:
            msg = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.chat_message("assistant").write(msg)
    else:
        raise ValueError("No response from OpenAI API")
