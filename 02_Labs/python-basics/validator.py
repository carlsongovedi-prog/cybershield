def validate_text(value, max_length=4000):
    if not isinstance(value, str):
        raise TypeError("Input must be text")
    if not value.strip():
        raise ValueError("Input must not be empty")
    if len(value) > max_length:
        raise ValueError("Input is too long")
    return value
