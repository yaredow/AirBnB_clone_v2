#!/usr/bin/python3
"""Script that starts a Flask web application"""

from flask import Flask, render_template
from models import storage
app = Flask(__name__)


@app.route("/states/<id>", strict_slashes=False)
def states_by_id(id):
    """Display States by id"""
    for state in storage.all('State').values():
        if state.id == id:
            return render_template('9-states.html', state=state)
    return render_template('9-states.html')


@app.route('/states', strict_slashes=False)
def states_all():
    """Display States"""
    states = storage.all('State')
    return render_template('9-states.html', state=states)


@app.teardown_appcontext
def teardown_db(self):
    """Remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
