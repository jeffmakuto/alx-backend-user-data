#!/usr/bin/env python3
""" Flask app """
from flask import Flask, jsonify, request
from typing import Dict
from auth import Auth


app = Flask(__name__)
app.url_map.strict_slashes = False
AUTH = Auth()

@app.route('/', methods=['GET'])
def welcome() -> Dict[str, str]:
    """
    Returns a JSON response with a welcome message.

    Returns:
        dict: A dictionary containing a welcome message.
    """
    return jsonify({"message": "Bienvenue"})

@app.route('/users', methods=['POST'])
def users(email: str, password: str) -> Dict[str, str]:
    """
    Register a new user.

    Expects form data with 'email' and 'password' fields.

    Returns:
        str: A JSON string containing a success message
             or an error message if registration fails.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
