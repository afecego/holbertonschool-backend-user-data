#!/usr/bin/env python3
""" function that expects one string argument name password."""
import bcrypt


def hash_password(password: str) -> bytes:
    """returns a salted, hashed password, which is a byte string"""
    salt = bcrypt.gensalt()
    bytePwd = password.encode('utf-8')
    hashed = bcrypt.hashpw(bytePwd, salt)
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ validate that the provided password matches the hashed password"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
