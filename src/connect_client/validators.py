def validate_id(i):
    if not isinstance(i, int) or i <= 0:
        raise ValueError("ID must be a positive integer")


def validate_uid(u):
    if not isinstance(u, str) or not u.strip():
        raise ValueError("UID must be a non-empty string")
