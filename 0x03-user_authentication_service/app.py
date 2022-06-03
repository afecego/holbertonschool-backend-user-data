#!/usr/bin/env python3
"""set up a basic Flask app"""
from flask import Flask, jsonify, request
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
    email = request.form['email']
    password = request.form['password']

    try:
        if AUTH.register_user(email, password) is not None:
            payload = {f"email": {email}, "message": "user created"}
            return jsonify(payload)
    except ValueError:
        no_payload = {"message": "email already registered"}
        return jsonify(no_payload), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
