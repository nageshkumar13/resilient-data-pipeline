def validate_email(email: str) -> bool:
    """Return True when an email looks valid."""
    if not isinstance(email, str):
        return False

    email = email.strip()
    if not email:
        return False

    if email.count("@") != 1:
        return False

    local_part, domain_part = email.split("@", 1)
    if not local_part or not domain_part:
        return False

    if "." not in domain_part:
        return False

    if " " in email:
        return False

    return True
