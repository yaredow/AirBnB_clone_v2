#!/usr/bin/python3
"""
script that starts a Flask web application:
- web application must be listening on 0.0.0.0, port 5000
- Routes:
- /: display “Hello HBNB!”
- /hbnb: display "HBNB"
- /c/<text>: display “C ”, followed by the value of the text variable
- python/<text>: display “Python ”, followed by the value of the text variable
- /number/<n>: display “n is a number” only if n is an integer
- use the option strict_slashes=False in your route definition
"""

from flask import Flask


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello_route():
    """Flask web application that displays 'Hello HBNB' at route:'/' """
    return "Hello HBNB!"


@app.route('/hbnb')
def HBNB_route():
    """Flask web application that displays 'HBNB' at route:'/hbnb' """
    return "HBNB"


@app.route('/c/<text>')
def c_route(text):
    """/c/<text>: display “C ”, followed by the value of the text variable
(replace underscore _ symbols with a space)"""
    return "C " + text.replace("_", " ")


@app.route('/python', defaults={'text': 'is cool'})
@app.route('/python/<text>')
def python_route(text):
    """/python/<text>: display “Python ”, followed by the value of the
text variable (replace underscore _ symbols with a space )"""
    return "Python " + text.replace("_", " ")


@app.route('/number/<int:n>')
def number_route(n):
    """/number/<n>: display “n is a number” only if n is an integer"""
    return "{} is a number".format(n)


if __name__ == "__main__":
    app.run()
