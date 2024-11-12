def prepare_prompt(prompt_template_path, **kwargs):
    """
    Replace the placeholders in the prompt template with the given values.
    Args:
        prompt_template_path (str): The path to the prompt template file.
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
