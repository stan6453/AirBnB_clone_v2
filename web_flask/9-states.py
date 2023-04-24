#!/usr/bin/python3
"""Flask web application"""

from models import storage
from models.state import State
from flask import Flask, render_template

app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception):
    """Reload the current SQLAlchemy session"""
    storage.close()


@app.route('/states', strict_slashes=False)
def list_states():
    """/states route"""
    return render_template('9-states.html', states=storage.all(State))


@app.route('/states/<string:id>', strict_slashes=False)
def list_cities(id=None):
    """/states/<id> route"""
    states = storage.all(State).values()
    state = None
    for item in states:
        if item.id == id:
            state = item
    return render_template('9-states.html', state=state)


if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
