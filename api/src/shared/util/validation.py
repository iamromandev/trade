import re


def validate_password(password: str) -> list[str]:
    errors: list[str] = []

    if len(password) < 12 or len(password) > 128:
        errors.append("Password must be between 12 and 128 characters")

    if not all(32 <= ord(c) <= 126 for c in password):
        errors.append("Password must only contain printable ASCII characters")

    categories = 0
    if re.search(r"[a-z]", password):
        categories += 1
    if re.search(r"[A-Z]", password):
        categories += 1
    if re.search(r"\d", password):
        categories += 1
    if re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]", password):
        categories += 1

    if categories < 3:
        errors.append("Password must contain at least 3 of: lowercase, uppercase, digits, symbols")

    return errors
