#!/usr/bin/python3
"""
Start the flask application server listening on 0.0.0.0, port 5000
    when the user hits the route /cities_by_states, it will response
    with html page that contains all the state and its cities in
    database hbnb_dev_db

    thsee environment variables should be present:
    HBNB_MYSQL_USER=hbnb_dev
    HBNB_MYSQL_PWD=hbnb_dev_pwd
    HBNB_MYSQL_HOST=localhost
    HBNB_MYSQL_DB=hbnb_dev_db
    HBNB_TYPE_STORAGE=db

    the sql script setup_mysql_dev.sql creates the database
    if it doesn't exist
"""

from flask import Flask, render_template
from models import storage

app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


@app.route("/cities_by_states", strict_slashes=False)
def states_list():
    """The view for the url routing to the html file
            8-cities_by_states.html, in this format

    /cities_by_states: display a HTML page: (inside the tag BODY)
    H1 tag: “States”
    UL tag: with the list of all State objects present in DBStorage
    sorted by name (A->Z)
    LI tag: description of one State:
    <state.id>: <B><state.name></B>
    + UL tag: with the list of City objects linked to the State
    sorted by name (A->Z)
    LI tag: description of one City:
    <city.id>: <B><city.name></B>
    """

    state_objs = storage.all("State")
    if storage.__class__.__name__ == "FileStorage":
        flag = True
    else:
        flag = False
    return render_template(
        "8-cities_by_states.html", state_objs=state_objs, flag=flag
        )


@app.teardown_appcontext
def teardown(exc):
    """Remove the current SQLAlchemy session."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
