import bcrypt


def _truncate(password: str) -> bytes:
    """bcrypt truncates at 72 bytes — do it explicitly."""
    return password.encode("utf-8")[:72]


def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(_truncate(password), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(_truncate(password), hashed.encode("utf-8"))