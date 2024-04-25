#!/usr/bin/env python3
""" Auth module """


def _hash_password(password: str) -> str:
    """
    Takes in a password string arguments
    and returns bytes.

    Args:
        password (str): password

    Return:
        string bytes - salted hashed
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
