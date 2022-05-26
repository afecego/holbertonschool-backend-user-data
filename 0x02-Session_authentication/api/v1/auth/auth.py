#!/usr/bin/env python3
"""manage the API authentication"""
from typing import List, TypeVar
from flask import request


class Auth:
    """template for all authentication system"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns False - path and excluded_paths"""
        if path is None:
            return True
        if not excluded_paths or excluded_paths is None:
            return True
        if path in excluded_paths:
            return False
        for i in excluded_paths:
            if i.endswith('*'):
                a = i[0:-1]
                if a in path:
                    return False
            if path in i[0:-1]:
                return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """returns None - request will be the Flask request object"""
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None - request will be the Flask request object"""
        return None

    def session_cookie(self, request=None):
        """returns a cookie value from a request"""
        if request is not None:
            return None
        
