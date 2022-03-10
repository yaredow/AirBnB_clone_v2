#!/usr/bin/python3
"""  a script that starts a Flask web application: """

from flask import Flask, render_template
from models import storage
from models import State
app = Flask(__name__)


@app.teardown_appcontext
def closedb(argument):
    """ to close a database session"""
    storage.close()


@app.route('/states', strict_slashes=False, defaults={'id': None})
@app.route('/states/<id>', strict_slashes=False)
def states(id):
    """ /states route """
    state = states = None
    if not id:
        states = list(storage.all(State).values())
    else:
        states = storage.all(State)
        key = "State." + id
        if key in states:
            state = states[key]
        else:
            state = None
        states = []
    return render_template('9-states.html', **locals())


if __name__ == '__main__':
    storage.reload()
    app.run("0.0.0.0", 5000)
