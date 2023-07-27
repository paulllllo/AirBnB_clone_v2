#!/usr/bin/python3
"""
Flask module to run the web application and render
on /state_list.
"""
from models import storage
from models.state import State
from flask import Flask, render_template


app = Flask(__name__)


@app.teardown_appcontext
def close_session(exception=None):
    """Close the current session."""
    storage.close()


@app.route('/states_list', strict_slashes=False)
def list_state():
    """Render list of all states."""
    states_list = storage.all(State)
    return render_template('7-states_list.html', states=states_list)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
