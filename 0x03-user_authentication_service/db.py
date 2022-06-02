#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """method should save the user to the database"""
        if email is None or type(email) is not str:
            return None
        if hashed_password is None or type(hashed_password) is not str:
            return None
        us = User(email=email, hashed_password=hashed_password)
        self._session.add(us)
        self._session.commit()
        return us

    def find_user_by(self, **kwargs: str) -> User:
        """returns the first row found in the users table as filtered by the
        method’s input arguments"""
        try:
            filt = self._session.query(User).filter_by(**kwargs).first()
        except InvalidRequestError:
            raise InvalidRequestError
        if filt is None:
            raise NoResultFound
        return filt
