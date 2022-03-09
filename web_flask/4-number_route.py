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
    val = text.replace('_', ' ')
    return 'C {}'.format(val)


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python(text='is cool'):
    """Python"""
    val = text.replace('_', ' ')
    return "Python {}". format(val)


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """Number"""
    return '{} is a number'.format(n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
