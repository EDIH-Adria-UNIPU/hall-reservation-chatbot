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
                "name": ChatFunctions.COLLECT_CONTACT.value,
                "description": "Collects contact information from the user for sending an offer",
                "strict": True,
                "parameters": {
                    "type": "object",
                    "required": ["name", "contact_type", "contact_value", "space_type", "requirements"],
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name of the person requesting the offer",
                        },
                        "contact_type": {
                            "type": "string",
                            "description": "The preferred contact method (email or phone)",
                            "enum": ["email", "phone"],
                        },
                        "contact_value": {
                            "type": "string",
                            "description": "The email address or phone number",
                        },
                        "space_type": {
                            "type": "string",
                            "description": "Type of space they're interested in",
                            "enum": ["konferencijska_dvorana", "sala_za_sastanke", "ured", "flydesk"],
                        },
                        "requirements": {
                            "type": "object",
                            "description": "All the requirements collected during the conversation",
                            "properties": {
                                "participants": {
                                    "type": "integer",
                                    "description": "Number of participants/workspaces needed",
                                },
                                "date": {
                                    "type": "string",
                                    "description": "Desired date for the space",
                                },
                                "time": {
                                    "type": "string",
                                    "description": "Desired time for the space",
                                },
                                "additional_services": {
                                    "type": "array",
                                    "items": {
                                        "type": "string"
                                    },
                                    "description": "List of additional services needed",
                                },
                                "duration": {
                                    "type": "string",
                                    "description": "Duration of stay (for flydesk)",
                                },
                                "tour_requested": {
                                    "type": "boolean",
                                    "description": "Whether they want to schedule a tour",
                                },
                                "how_found": {
                                    "type": "string",
                                    "description": "How they found out about the coworking space",
                                }
                            },
                            "required": [
                                "participants",
                                "date",
                                "time",
                                "additional_services",
                                "duration",
                                "tour_requested",
                                "how_found"
                            ],
                            "additionalProperties": False,
                        }
                    },
                    "additionalProperties": False,
                },
            },
        }
    ]
