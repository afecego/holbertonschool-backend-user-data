#!/usr/bin/env python3
""" Module of Sesion_auth views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session() -> str:
    """ POST /api/v1/auth_session/login
    """
    in_email = request.form.get('email')
    in_password = request.form.get('password')

    if not in_email:
        return jsonify({"error": "email missing"}), 400
    if not in_password:
        return jsonify({"error": "password missing"}), 400
    try:
        data = User.search({'email': in_email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404
    if not data:
        return jsonify({"error": "no user found for this email"}), 404
    for i in data:
        if not i.is_valid_password(in_password):
            return jsonify({"error": "wrong password"}), 401
    resum = data[0]
    from api.v1.app import auth
    cookie = os.getenv('SESSION_NAME')
    session = auth.create_session(resum.id)
    out = jsonify(resum.to_json())
    out.set_cookie(cookie, session)
    return out


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def del_session() -> str:
    """Delete the session"""
    from api.v1.app import auth
    delet = auth.destroy_session(request)
    if not delet:
        abort(404)
    return jsonify({}), 200
