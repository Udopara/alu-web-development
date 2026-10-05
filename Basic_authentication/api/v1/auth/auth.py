#!/usr/bin/env python3
""" Auth module for managing API authentication logic
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Auth class template for managing authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Determine whether a given path requires authentication

        Returns True if path is None, excluded_paths is None/empty, or path is
        not in excluded_paths. Returns False if path is in excluded_paths.
        Method is slash-tolerant.
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        path_slash = path if path.endswith('/') else path + '/'

        for excluded in excluded_paths:
            if excluded.endswith('/'):
                if path_slash == excluded:
                    return False
            else:
                if path == excluded or path_slash == excluded + '/':
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Retrieve Authorization header value from request
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """ Retrieve current User instance from request
        """
        return None
