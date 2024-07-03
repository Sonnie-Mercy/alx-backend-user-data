#!/usr/bin/env python3
"""
encrypt_password module
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash a password with a random salt.

    Args:
        password (str): The plain text password to hash.

    Returns:
        bytes: The salted, hashed password as a byte string.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed

def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    validating if the provided password matches the hashed password
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
