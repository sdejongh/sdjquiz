def is_valid_input_count(text_input: str or None):
    if text_input is None:
        return False
    return text_input.isdigit() or text_input == ""
