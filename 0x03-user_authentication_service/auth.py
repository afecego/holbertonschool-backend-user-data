#!/usr/bin/env python3
"""define a _hash_password method"""
import bcrypt
from user import User
from sqlalchemy.orm.exc import NoResultFound
from db import DB


def _hash_password(password: str) -> bytes:
    """takes in a password string arguments and returns bytes"""
    salt = bcrypt.gensalt()
    bytePwd = password.encode('utf-8')
    hashed = bcrypt.hashpw(bytePwd, salt)
    return hashed


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ake mandatory email and password string arguments and return a
        User object."""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists.')
        except NoResultFound:
            hash_pass = _hash_password(password)
            user = self._db.add_user(email, hash_pass)
            return user
