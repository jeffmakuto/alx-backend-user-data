#!/usr/bin/env python3
""" Flask app """
from flask import Flask, jsonify
from typing import Dict


app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route('/', methods=['GET'])
def welcome() -> Dict[str, str]:
    """
    Returns a JSON response with a welcome message.

    Returns:
        dict: A dictionary containing a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
