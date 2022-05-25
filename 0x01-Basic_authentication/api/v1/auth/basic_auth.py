#!/usr/bin/env python3
"""class BasicAuth"""
import base64
import binascii
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """that inherits from Auth"""
    def extract_base64_authorization_header(self, authorization_header:
                                            str) -> str:
        """returns the Base64 part of the Authorization header for a
        Basic Authentication:"""
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if authorization_header.startswith('Basic '):
            return authorization_header[6:]
        return None

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """return the decoded value as UTF8 string - you can use
        decode('utf-8')"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            decod = base64.b64decode(base64_authorization_header)
            return decod.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """returns the user email and password from the Base64 decoded value"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) is not str:
            return (None, None)
        if ':' in decoded_base64_authorization_header:
            a = decoded_base64_authorization_header.split(':')
            (b, c) = (a[0], a[1])
            return (b, c)
        return (None, None)

    def user_object_from_credentials(self, user_email: str, user_pwd:
                                     str) -> TypeVar('User'):
        """ returns the User instance based on his email and password."""
        if type(user_email) is not str:
            return None
        if type(user_pwd) is not str:
            return None
        try:
            data = User.search({'email': user_email})
        except Exception:
            return None
        for i in data:
            if i.is_valid_password(user_pwd):
                return i
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """retrieves the User instance for a request"""
        basic_aut = self.authorization_header(request)
        extrac_base64 = self.extract_base64_authorization_header(basic_aut)
        decode = self.decode_base64_authorization_header(extrac_base64)
        (email, pwd) = self.extract_user_credentials(decode)
        user = self.user_object_from_credentials(email, pwd)
        return user
