#!/usr/bin/python3
"""ALX SE Flask Module."""
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/hbnb', strict_slashes=False)
def index_html_8():
    """Displays a html page like 8-index.html."""
    states_list = storage.all(State)
    amenities_list = storage.all(Amenity)
    places_list = storage.all(Place)
    return render_template(
            '100-hbnb.html', states=states_list, amenities=amenities_list, places=places_list)


@app.teardown_appcontext
def close_session(exception=None):
    """Close the current session."""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
