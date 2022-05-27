#!/usr/bin/env python3
"""Create a class SessionAuth"""
from api.v1.auth.auth import Auth
import uuid

from models.user import User


class SessionAuth(Auth):
    """inherits from Auth"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID for a user_id"""
        if user_id is None:
            return None
        if type(user_id) is not str:
            return None
        id = str(uuid.uuid4())
        self.user_id_by_session_id[id] = user_id
        return id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a User ID based on a Session ID"""
        if session_id is None:
            return None
        if type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ returns a User instance based on a cookie value"""
        cookie = self.session_cookie(request)
        data = self.user_id_for_session_id(cookie)
        user = User.get(data)
        return user

    def destroy_session(self, request=None):
        """deletes the user session / logout"""
        if request is None:
            return False
        if self.session_cookie(request) is None or self.user_id_for_session_id(
                self.session_cookie(request)) is None:
            return False
        del self.user_id_by_session_id[self.session_cookie(request)]
        return True
