#!/usr/bin/python3
"""Flask web application"""

from flask import Flask, render_template

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
def mypy(text='is cool'):
    """/python/<text> route"""
    return 'Python {}'.format(' '.join(text.split('_')))


@app.route('/number/<int:n>', strict_slashes=False)
def check_num(n):
    """/number/<int:n> route"""
    return '{} is a number'.format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def display_num(n):
    """/number_template/<n> route"""
    return render_template('5-number.html', number=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def even_odd(n):
    """/number_odd_or_even/<n> route"""
    return render_template('6-number_odd_or_even.html', number=n)


if __name__ == '__main__':
    app.run('0.0.0.0', 5000)

