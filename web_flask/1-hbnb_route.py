#!/usr/bin/python3
"""
Start the flask application server listening on 0.0.0.0, port 5000
and display 'Hello HBNB!' on /
and display 'HBNB' on /hbnb
"""

from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def index():
    """ The view for the url routing to the root of the page

        return: html page with the text Hello HBNB!
    """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """The view for the url routing to the /hbnb of the page

    return: html page with the text HBNB
    """
    return "HBNB"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
