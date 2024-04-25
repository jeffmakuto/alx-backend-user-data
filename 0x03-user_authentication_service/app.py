#!/usr/bin/env python3
""" Flask app """
from flask import Flask, jsonify, request, abort
from auth import Auth


app = Flask(__name__)
app.url_map.strict_slashes = False
AUTH = Auth()

@app.route('/', methods=['GET'])
def welcome() -> str:
    """
    Returns a JSON response with a welcome message.

    Returns:
        dict: A dictionary containing a welcome message.
    """
    return jsonify({"message": "Bienvenue"})

@app.route('/users', methods=['POST'])
def users() -> str:
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

@app.route('/sessions', methods=['POST'])
def login() -> str:
    """
    Returns request with form data with email and password fields
    """
    user_request = request.form
    user_email = user_request.get('email', '')
    user_password = user_request.get('password', '')
    valid_log = AUTH.valid_login(user_email, user_password)
    if not valid_log:
        abort(401)
    response = make_response(jsonify({"email": user_email,
                                      "message": "logged in"}))
    response.set_cookie('session_id', AUTH.create_session(user_email))
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
