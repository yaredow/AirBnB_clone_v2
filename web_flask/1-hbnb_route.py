#!/usr/bin/python3
"""  a script that starts a Flask web application """

from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """ index """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ hbnb route """
    return "HBNB"

if __name__ == '__main__':
    app.run("0.0.0.0", 5000)
