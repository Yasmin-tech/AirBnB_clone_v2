#!/usr/bin/python3
"""
Start the flask application server listening on 0.0.0.0, port 5000
    when the user hits the route /states_list, it will response
    with html page that contains all the state in the database hbnb_dev_db

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


@app.route("/states_list", strict_slashes=False)
def states_list():
    """The view for the url routing to the html file
        7-states_list.html, in this format

    (inside the tag BODY)
    H1 tag: “States”
    UL tag: with the list of all State objects present in DBStorage
    sorted by name (A->Z)
    LI tag: description of one State: <state.id>: <B><state.name></B>
    """

    state_objs = storage.all("State")
    return render_template("7-states_list.html", state_objs=state_objs)


@app.teardown_appcontext
def teardown(exc):
    """Remove the current SQLAlchemy session."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
