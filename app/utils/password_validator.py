import re
from fastapi import HTTPException


def validate_password(password: str):

    # bcrypt safe byte limit
    if len(password.encode("utf-8")) > 72:
        raise HTTPException(
            400,
            "Password too long. Maximum allowed length is 72 bytes."
        )

    if len(password) < 8:
        raise HTTPException(400, "Password must be at least 8 characters")

    if not re.search(r"[A-Z]", password):
        raise HTTPException(400, "Password must contain uppercase letter")

    if not re.search(r"[a-z]", password):
        raise HTTPException(400, "Password must contain lowercase letter")

    if not re.search(r"\d", password):
        raise HTTPException(400, "Password must contain number")

    if not re.search(r"[!@#$%^&*()_+=\-{}[\]:;\"'<>,.?/]", password):
        raise HTTPException(400, "Password must contain special character")
