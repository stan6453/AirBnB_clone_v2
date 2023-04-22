#!/usr/bin/python3
"""Flask web application"""

from models import storage
from models.state import State
from flask import Flask, render_template

app = Flask(__name__)


@app.teardown_appcontext
def tearItDown(exception):
    """Reload the current SQLAlchemy session"""
    storage.close()


@app.route('/states_list', strict_slashes=False)
def list_states():
    """/states_list route"""
    states = storage.all(State)
    return render_template('7-states_list.html', states=states)


if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
