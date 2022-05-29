#!/usr/bin/env python3
"""Create a class SessionExpAuth"""
from datetime import datetime, timedelta
import os
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """inherits from SessionAuth"""
    def __init__(self):
        """Overload method"""
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """create session"""
        if type(user_id) is not str:
            return None
        try:
            session = super().create_session(user_id)
        except Exception:
            return None

        session_dictionary = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session] = session_dictionary
        return session

    def user_id_for_session_id(self, session_id=None):
        """return user_id from the session dictionary"""
        if session_id is None:
            return None
        if type(session_id) is not str:
            return None
        diction = self.user_id_by_session_id.get(session_id)
        if not diction or diction is None:
            return None
        if self.session_duration <= 0:
            return diction.get('user_id')
        if 'created_at' is not diction:
            return None

        time = diction.get('created_at')
        session_connect = timedelta(seconds=self.session_duration)

        if time + session_connect < datetime.now():
            return None
        else:
            return diction.get('user_id')
