#!/usr/bin/env python3
""" BasicAuth module for Basic Authentication
"""
import base64
from typing import TypeVar, Tuple
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """ BasicAuth class inheriting from Auth
    """

    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:
        """ Extract Base64 part of Authorization header for Basic Auth
        """
        if authorization_header is None or not isinstance(
            authorization_header, str
        ):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """ Decode a Base64 authorization header string into UTF-8
        """
        if base64_authorization_header is None or not isinstance(
            base64_authorization_header, str
        ):
            return None
        try:
            decoded_bytes = base64.b64decode(
                base64_authorization_header.encode('utf-8')
            )
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> Tuple[str, str]:
        """ Extract user email and password from decoded Base64 string
        """
        if (
            decoded_base64_authorization_header is None
            or not isinstance(decoded_base64_authorization_header, str)
        ):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        parts = decoded_base64_authorization_header.split(':', 1)
        return (parts[0], parts[1])

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar('User'):
        """ Retrieve User instance matching email and valid password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        users = User.search({'email': user_email})
        if not users or len(users) == 0:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Overload current_user to retrieve User instance from request
        """
        auth_header = self.authorization_header(request)
        b64_header = self.extract_base64_authorization_header(auth_header)
        decoded_b64 = self.decode_base64_authorization_header(b64_header)
        email, password = self.extract_user_credentials(decoded_b64)
        return self.user_object_from_credentials(email, password)
