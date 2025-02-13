import streamlit as st
from openai import OpenAI
import os
import json
from datetime import datetime

from utils import prepare_prompt, get_available_tools
from data_manager import DataManager
from functions import ChatFunctions

# Create calendar.json if it doesn't exist
calendar_path = "calendar.json"
if not os.path.exists(calendar_path):
    initial_calendar = {
        "dvorana": {},
        "sala_za_sastanke": {},
        "ured": {}
    }
    with open(calendar_path, "w") as f:
        json.dump(initial_calendar, f)

st.image("src/assets/ida_logo.jpg", width=200)

st.title("Chatbot za rezevaciju prostora")

manager = DataManager()
manager.add_dummy_bookings()  # Initialize some dummy bookings for testing
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

    initial_assistant_msg = {
        "role": "assistant",
        "content": "Pozdrav! Ja sam asistent za rezervaciju prostora u Coworking Pula. Mogu vam pomoći s informacijama o najmu konferencijske dvorane, sale za sastanke, ureda ili radnih jedinica (flydesk). Koji prostor vas zanima?",
    }

    st.session_state.messages.append(initial_assistant_msg)

for msg in st.session_state.messages:
    if isinstance(msg, dict) and msg["role"] in ["user", "assistant"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            # Show parking image if assistant mentions parking
            if msg["role"] == "assistant" and "parking" in msg["content"].lower():
                st.image("src/assets/parking.png", caption="Parking lokacija")


def handle_function_call(manager, function_name, arguments):
    if function_name == ChatFunctions.COLLECT_CONTACT.value:
        result = manager.collect_contact(
            arguments.get("name"),
            arguments.get("contact_type"),
            arguments.get("contact_value"),
            arguments.get("space_type"),
            arguments.get("requirements"),
        )
        print("\nContact information collected:", result)
    elif function_name == ChatFunctions.CHECK_AVAILABILITY.value:
        result = manager.check_availability(
            arguments.get("space_type"),
            arguments.get("date"),
            arguments.get("start_time"),
            arguments.get("end_time")
        )
        print("\nAvailability check result:", result)
        return "Prostor je dostupan u traženom terminu." if result else "Nažalost, prostor nije dostupan u traženom terminu."
    else:
        raise ValueError(f"Function '{function_name}' not found.")
    return result


def retrieve_function_details(response):
    tool_call = response.choices[0].message.tool_calls[0]
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)
    return tool_call, function_name, arguments


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
        with st.chat_message("assistant"):
            st.write(msg)
            # Show parking image immediately if mentioned
            if "parking" in msg.lower():
                st.image("src/assets/parking.png", caption="Parking lokacija")
    elif response.choices[0].message.tool_calls:
        tool_call, function_name, arguments = retrieve_function_details(response)

        print(f"\nCall function {function_name} with arguments: {arguments}")
        result = handle_function_call(manager, function_name, arguments)

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
            with st.chat_message("assistant"):
                st.write(msg)
                # Show parking image immediately if mentioned
                if "parking" in msg.lower():
                    st.image("src/assets/parking.png", caption="Parking lokacija")
    else:
        raise ValueError("No response from OpenAI API")
