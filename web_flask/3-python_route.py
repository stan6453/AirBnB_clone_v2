#!/usr/bin/python3
"""Flask web application"""

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """base route"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """hbnb route"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def Cee(text):
    """/c/<text> route"""
    return 'C {}'.format(' '.join(text.split('_')))


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def mypy(text=None):
    """/python/<text> route"""
    if text:
        return 'Python {}'.format(' '.join(text.split('_')))
    return 'Python is cool'


if __name__ == '__main__':
    app.run('0.0.0.0', 5000)

