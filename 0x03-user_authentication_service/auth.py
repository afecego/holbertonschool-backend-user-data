#!/usr/bin/env python3
"""define a _hash_password method"""
from typing import Union
import uuid
import bcrypt
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session
from db import DB


def _hash_password(password: str) -> bytes:
    """takes in a password string arguments and returns bytes"""
    salt = bcrypt.gensalt()
    bytePwd = password.encode('utf-8')
    hashed = bcrypt.hashpw(bytePwd, salt)
    return hashed


def _generate_uuid() -> str:
    """return a string representation of a new UUID"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """method initial"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Make mandatory email and password str arguments
        and return a User object."""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exist')
        except NoResultFound:
            hash_pass = _hash_password(password)
            user = self._db.add_user(email, hash_pass)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Validation of credentials"""
        try:
            cred = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  cred.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> Session:
        """find the user corresponding to the email, generate a
        new UUID and store it in the database"""
        try:
            us = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(us.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """returns the corresponding User or None"""
        if session_id is None:
            return None
        try:
            found = self._db.find_user_by(session_id=session_id)
            return found
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """takes a single user_id integer argument and returns None"""
        if user_id is None:
            return None
        try:
            found = self._db.find_user_by(id=user_id)
            self._db.update_user(found.id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """take an email string argument and returns a string."""
        try:
            us = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(us.id, reset_token=token)
            return token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """takes reset_token string argument and a password string
        argument and returns None"""
        try:
            us = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        hashset = _hash_password(password)
        self._db.update_user(us.id, hashed_password=hashset, reset_token=None)
