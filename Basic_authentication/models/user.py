#!/usr/bin/env python3
""" User module for managing User data model
"""
import hashlib
from models.base import Base


class User(Base):
    """ User class representing system users
    """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a User instance
        """
        super().__init__(*args, **kwargs)
        self.email = kwargs.get('email', None)
        self._password = kwargs.get('_password', None)
        self.first_name = kwargs.get('first_name', None)
        self.last_name = kwargs.get('last_name', None)

    @property
    def password(self) -> str:
        """ Password getter
        """
        return self._password

    @password.setter
    def password(self, pwd: str):
        """ Password setter with SHA256 hashing
        """
        if pwd is None or not isinstance(pwd, str):
            self._password = None
        else:
            self._password = hashlib.sha256(pwd.encode()).hexdigest().lower()

    def is_valid_password(self, pwd: str) -> bool:
        """ Check if provided clear password matches stored hashed password
        """
        if pwd is None or not isinstance(pwd, str):
            return False
        if self._password is None:
            return False
        pwd_h = hashlib.sha256(pwd.encode()).hexdigest().lower()
        return pwd_h == self._password

    def display_name(self) -> str:
        """ Display name formatting for User
        """
        if (
            self.email is None
            and self.first_name is None
            and self.last_name is None
        ):
            return ""
        if self.first_name is None and self.last_name is None:
            return self.email
        if self.first_name is None:
            return self.last_name
        if self.last_name is None:
            return self.first_name
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def search(cls, attributes: dict = {}) -> list:
        """ Search users matching specified attribute criteria
        """
        from models import storage
        return storage.search(cls, attributes)

    @classmethod
    def count(cls) -> int:
        """ Count total User objects stored
        """
        from models import storage
        return storage.count(cls)

    @classmethod
    def get(cls, id: str):
        """ Retrieve a User object by ID
        """
        from models import storage
        return storage.get(cls, id)
