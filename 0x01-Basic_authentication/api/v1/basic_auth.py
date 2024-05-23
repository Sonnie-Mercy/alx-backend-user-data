#!/usr/bin/env python3
"""
Module basic_auth
"""
from api.v1.auth.auth import Auth
import base64
import binascii
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    A class that represent BasicAuth
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extract the Base64 part of the Authorization header
           for a Basic Authentication

        Parameters
        ----------
        authorization_header: str
            authorization header

        Returns
        ------
        str
            the Base64 part of the Authorization header
        """
        if authorization_header is None or type(authorization_header) != str:
            return
        if not authorization_header.startswith("Basic "):
            return
        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """Reterive the decoded value of a Base64 string
           base64_authorization_header

        Parameters
        ---------
        base64_authorization_header: str
            base64 authorization header

        Returns
        -------
        str:
            decoded value of a Base64 string
        """
        if base64_authorization_header is None\
           or type(base64_authorization_header) != str:
            return
        try:
            byte_result = base64.b64decode(base64_authorization_header)
            str_result = byte_result.decode("utf-8")
        except binascii.Error as e:
            return
        return str_result

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """Extract the user email and password from the Base64 decoded value

        Parameters
        ---------
        decoded_base64_authorization_header: str
            decode base64 authorization header

        Returns: tuple
        -------
            user credentails email and password
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) != str:
            return (None, None)
        if not decoded_base64_authorization_header.__contains__(":"):
            return (None, None)
        new_list = decoded_base64_authorization_header.split(":")
        return (new_list[0], ":".join(new_list[1:]))

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Extract the User instance based on his email and password

        Parameters
        ---------
        user_email: str
            user email
        user_pwd: str
            user password

        Returns
        -------
        User
            object type of User
        """
        if user_email is None or type(user_email) != str:
            return
        if user_pwd is None or type(user_pwd) != str:
            return
        try:
            user = User.search({'email': user_email})
        except Exception:
            return None
        if len(user) == 0:
            return None
        valid_pass = user[0].is_valid_password(user_pwd)
        if not valid_pass:
            return None
        return user[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """Reterive User object

        Parameters
        ----------
        request: object
            request object found when http request is sent

        Returns
        -------
        object
            user objecct
        """
        header = self.authorization_header(request)
        authorization = self.extract_base64_authorization_header(header)
        _decode = self.decode_base64_authorization_header(authorization)
        credential = self.extract_user_credentials(_decode)
        return self.user_object_from_credentials(credential[0], credential[1])
