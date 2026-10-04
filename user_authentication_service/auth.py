#!/usr/bin/env python3
"""Auth module for user authentication and session management.
"""
import bcrypt
from typing import Optional
import uuid

from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User


def _hash_password(password: str) -> str:
    """Hash a password string using bcrypt with salt and return string.
    """
    return bcrypt.hashpw(password.encode('utf-8'),
                         bcrypt.gensalt()).decode('utf-8')


def _generate_uuid() -> str:
    """Generate and return a string representation of a new UUID.
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self) -> None:
        """Initialize Auth instance with private DB database object.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user if they don't already exist.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_pw = _hash_password(password)
            return self._db.add_user(email, hashed_pw)

    def valid_login(self, email: str, password: str) -> bool:
        """Validate user email and password credentials.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password.encode('utf-8'))
        except NoResultFound:
            return False

    def create_session(self, email: str) -> Optional[str]:
        """Create a new session for the user corresponding to email.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """Retrieve User object corresponding to the given session_id.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy session by setting session_id to None for user_id.
        """
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """Generate and store a reset password token for user by email.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError(f"User with email {email} does not exist")

        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Update user password using a reset token.
        """
        if reset_token is None or not isinstance(reset_token, str):
            raise ValueError("Invalid reset token")

        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError("Invalid reset token")

        hashed_pw = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed_pw,
                             reset_token=None)
