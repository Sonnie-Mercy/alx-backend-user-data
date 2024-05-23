#!/usr/bin/env python3
"""
Module auth

"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    A class that represent Authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Define which route don't need authentication

        Parameters
        ----------
        path: str
            endpoint to accessa resourec in Rest API
        Returns
        ------
        bool
            True if path not in excluded_paths or if it needs authentication
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if f'{path}/' in excluded_paths or path in excluded_paths:
            return False
        for route in excluded_paths:
            if route.__contains__("*") and route[:-1] in path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Reterive value of Authorization header

        Parameters
        ----------
        request: object
            request object found when http request is sent
        """
        if request is None:
            return
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """current user
        """
        return
