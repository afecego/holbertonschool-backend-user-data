#!/usr/bin/env python3
"""set up a basic Flask app"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def index():
    """return a JSON payload"""
    form = {"message": "Bienvenue"}
    return jsonify(form)


@app.route('/users', methods=['POST'])
def users():
    """end-point to register a user"""
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        regis = AUTH.register_user(email, password)
        if regis is not None:
            payload = {"email": regis.email, "message": "user created"}
            return jsonify(payload)
    except ValueError:
        no_payload = {"message": "email already registered"}
        return jsonify(no_payload), 400


@app.route('/sessions', methods=['POST'])
def login():
    """login function to respond to the POST /sessions route"""
    email = request.form['email']
    password = request.form['password']

    if not AUTH.valid_login(email, password):
        abort(401)
    else:
        new_session = AUTH.create_session(email)
        payload = jsonify({"email": email, "message": "logged in"})
        payload.set_cookie("session_id", new_session)
        return payload


@app.route('/sessions', methods=['DELETE'])
def logout():
    """function to respond to the DELETE /sessions route."""
    session = request.cookies['session_id']
    user = AUTH.get_user_from_session_id(session)
    if user is None or session in None:
        abort(403)
    else:
        AUTH.destroy_session(user.id)
        return redirect('/')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
