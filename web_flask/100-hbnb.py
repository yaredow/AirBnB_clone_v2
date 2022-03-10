#!/usr/bin/python3
"""  a script that starts a Flask web application: """

from flask import Flask, render_template
from models import storage
from models import State, Amenity, Place
app = Flask(__name__)


@app.teardown_appcontext
def closedb(argument):
    """ to close a database session"""
    storage.close()


@app.route('/hbnb', strict_slashes=False)
def hbnb_filters():
    """ /hbnb route """
    state = storage.all(State)
    amenities = storage.all(Amenity)
    place = storage.all(Place)
    return render_template('100-hbnb.html', **locals())


if __name__ == '__main__':
    storage.reload()
    app.run("0.0.0.0", 5000)
