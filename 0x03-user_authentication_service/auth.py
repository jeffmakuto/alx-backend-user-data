#!/usr/bin/env python3
""" Auth module """
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from db import DB
from user import User
import bcrypt
import uuid


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

def _generate_uuid() -> str:
    """
     return a string representation of a new UUID
     """
     return str(uuid.uuid4()) 


class Auth:
    """
    Auth class to interact with the authentication database.
    """
    def __init__(self) -> None:
        """
        Initialization
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
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

    def valid_login(self, email: str, password: str) -> bool:
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

    def create_session(self, email: str) -> str:
        """
        Takes an email string argument and returns the session ID as a string.
        The method should find the user corresponding to the email, generate
        a new UUID and store it in the database as the user’s session_id,
        then return the session ID.

        Args:
            email (str): email of user

        Returns:
            session ID as a string
        """
        session_id = _generate_uuid()
        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> str:
        """
        Takes single session_id string argument
        Returns corresponding User or None
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user.email
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Takes a single user_id integer srgument
        Returns None
        """
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Takes email string argument, Returns string
        Find user corresponding to email, raise ValueError if not exists
        generate uuid and update users reset_token database field
        Return the token if exists
        """
        updated_token = _generate_uuid()
        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, reset_token=updated_token)
            return updated_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> str:
        """Takes reset_token string argument and a password string
        returns None
        Use reset_token to find corresponding user, raise ValueError
        if doesnt exists, if exists, hash password and update user
        hashed_password field with new hashed password and reset_token
        field to None
        """
        if reset_token is None or password is None:
            return None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        hashed_password = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed_password,
                             reset_token=None)
