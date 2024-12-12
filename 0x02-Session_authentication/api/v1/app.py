#!/usr/bin/env python3
"""
API App
"""
from flask import Flask, jsonify, request, abort
from os import getenv

from api.v1.views import app_views
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth  # Import SessionAuth

app = Flask(__name__)
app.register_blueprint(app_views)

auth = None
auth_type = getenv('AUTH_TYPE')

if auth_type == "basic_auth":
    auth = BasicAuth()
elif auth_type == "session_auth":
    auth = SessionAuth()

@app.before_request
def before_request():
    """
    Filter requests before handling them.
    """
    if auth is None:
        return

    excluded_paths = ['/api/v1/status/',
                      '/api/v1/unauthorized/',
                      '/api/v1/forbidden/']

    if not auth.require_auth(request.path, excluded_paths):
        return

    if auth.authorization_header(request) is None and auth.session_cookie(request) is None:
        abort(401)

    request.current_user = auth.current_user(request)

    if request.current_user is None:
        abort(403)

@app.errorhandler(404)
def not_found(error):
    """404 Not Found handler."""
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorized(error):
    """401 Unauthorized handler."""
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error):
    """403 Forbidden handler."""
    return jsonify({"error": "Forbidden"}), 403

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = int(getenv("API_PORT", "5000"))
    app.run(host=host, port=port)
