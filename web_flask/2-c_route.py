#!/usr/bin/python3
"""Script that starts a Flask web application"""

from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """Hello"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """HBNB"""
    return 'HBNB'


@app.route('/c/<text>')
def var(text):
    """C"""
    return 'C {}'.format(text).replace('_', ' ')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
