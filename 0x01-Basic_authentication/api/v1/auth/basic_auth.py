#!/usr/bin/env python3
"""class BasicAuth"""
import base64
import binascii
from api.v1.auth.auth import Auth


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
        except binascii.Error:
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
