#!/usr/bin/env python3
"""DB module for database operations and SQLAlchemy session management.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class for managing database mapping and user model storage.
    """

    def __init__(self) -> None:
        """Initialize a new DB instance with SQLite engine and session manager.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized private session property.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database and return the User instance.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find and return the first user matching input keyword arguments.

        Raises:
            InvalidRequestError: If invalid column attribute names are passed.
            NoResultFound: If no user matching the criteria is found.
        """
        for key in kwargs:
            if not hasattr(User, key):
                raise InvalidRequestError(f"Invalid attribute {key}")

        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound("No result found")

        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update user attributes for the user matching user_id.

        Raises:
            ValueError: If an argument does not correspond to a User attribute.
            NoResultFound: If user with user_id is not found.
        """
        user = self.find_user_by(id=user_id)

        for key, value in kwargs.items():
            if not hasattr(User, key):
                raise ValueError(f"Invalid attribute {key}")
            setattr(user, key, value)

        self._session.commit()
