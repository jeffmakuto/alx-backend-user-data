#!/usr/bin/env python3
""" Auth module """
from db import DB


def _hash_password(password: str) -> str:
    """
    Takes in a password string arguments
    and returns bytes.

    Args:
        password (str): password

    Return:
        string bytes - salted hashed
    """
    return bcrypti.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """
    Auth class to interact with the authentication database.
    """
    def __init__(self) -> None:
        """
        Initialization
        """
        self._db = DB()

    def register_user(email: str, password: str) -> User:
        """
        Take mandatory email and password string arguments
        and return a User object.
        If a user already exist with the passed email, raise
        a ValueError with the message User <user's email> already exists.
        If not, hash the password with _hash_password,
        save the user to the database using self._db
        and return the User object.

        Args:
            email (str): email
            password (str): password

        Returns:
            User object
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists.".format(email))
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(email: str, password: str) -> bool:
        """
        Validate user login credentials.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            bool: True if the login is valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
        except NoResultFound:
            pass
        return False
