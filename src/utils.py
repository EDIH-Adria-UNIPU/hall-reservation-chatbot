from functions import ChatFunctions

def prepare_prompt(prompt_template_path: str, **kwargs) -> str:
    """
    Replace the placeholders in the prompt template with the given values.
    Args:
        prompt_template_path: The path to the prompt template file.
        **kwargs: Keyword arguments where keys are variable names (without '::')
                  and values are the replacement strings.
    Returns:
        str: The prompt
    """
    # Read the prompt template from the file
    with open(prompt_template_path, "r", encoding="utf-8") as file:
        prompt_template = file.read()

    prompt = prompt_template

    # Extract variables from the template
    template_parts = prompt_template.split("::")
    template_variables = [part.split()[0] for part in template_parts[1:]]

    # Check for unused variables
    passed_variables = set(kwargs.keys())
    template_variable_set = set(template_variables)
    unused_variables = passed_variables - template_variable_set

    if unused_variables:
        raise ValueError(
            f"The following variables were passed but not found in the template: {', '.join(unused_variables)}"
        )

    # Replace each variable with its corresponding value
    for variable, value in kwargs.items():
        placeholder = f"::{variable}"
        if placeholder not in prompt:
            raise ValueError(f"Variable '{variable}' not found in the prompt template.")
        prompt = prompt.replace(placeholder, value)

    return prompt


def get_available_tools() -> list:
    return [
        {
            "type": "function",
            "function": {
                "name": ChatFunctions.CHECK_AVAILABILITY.value,
                "description": "Filters availability by a specific date and a time range defined by start and end hours",
                "strict": True,
                "parameters": {
                    "type": "object",
                    "required": ["date", "start_hour", "end_hour"],
                    "properties": {
                        "date": {
                            "type": "string",
                            "description": "The date for which availability is being checked, formatted as YYYY-MM-DD",
                        },
                        "start_hour": {
                            "type": "number",
                            "description": "The starting hour for the time range (0-23)",
                        },
                        "end_hour": {
                            "type": "number",
                            "description": "The ending hour for the time range (0-23)",
                        },
                    },
                    "required": ["date", "start_hour", "end_hour"],
                    "additionalProperties": False,
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": ChatFunctions.MAKE_RESERVATION.value,
                "description": "Makes a reservation for a specified area type, date and time range",
                "strict": True,
                "parameters": {
                    "type": "object",
                    "required": ["area_type", "date", "start_hour", "end_hour"],
                    "properties": {
                        "area_type": {
                            "type": "string",
                            "description": "Type of area to reserve (hall, room, or coworking)",
                            "enum": ["hall", "room", "coworking"]
                        },
                        "date": {
                            "type": "string",
                            "description": "The date for the reservation, formatted as YYYY-MM-DD"
                        },
                        "start_hour": {
                            "type": "number",
                            "description": "The starting hour for the reservation (0-23)"
                        },
                        "end_hour": {
                            "type": "number",
                            "description": "The ending hour for the reservation (0-23)"
                        }
                    },
                    "additionalProperties": False
                }
            }
        }
    ]
