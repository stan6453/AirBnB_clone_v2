#!/usr/bin/python3
"""Flask web application"""

from models import storage
from models.state import State
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def list_states():
    """/cities_by_states route"""
    return render_template('8-cities_by_states.html', states=storage.all(State))


@app.teardown_appcontext
def teardown(exception):
    """Reload the current SQLAlchemy session"""
    storage.close()


if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
