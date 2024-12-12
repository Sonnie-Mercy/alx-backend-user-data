#!/usr/bin/env python3
"""
User view for API
"""
from flask import jsonify, abort, request
from models.user import User
from api.v1.views import app_views

@app_views.route('/api/v1/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieve all users."""
    users = [user.to_dict() for user in User.all()]
    return jsonify(users)

@app_views.route('/api/v1/users/me', methods=['GET'], strict_slashes=False)
def get_user_me():
    """
    Retrieve the authenticated user's information.
    """
    if request.current_user is None:
        abort(404)
    return jsonify(request.current_user.to_dict())

@app_views.route('/api/v1/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieve a user by ID."""
    if user_id == "me":
        if request.current_user is None:
            abort(404)
        return jsonify(request.current_user.to_dict())

    user = User.get(user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())
