#!/usr/bin/python3
"""
Start the flask application server listening on 0.0.0.0, port 5000
and display 'Hello HBNB!' on /
and display 'HBNB' on /hbnb
and display C followed by a variable passed to the route /c/<vaiable>
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


@app.route("/c/<text>", strict_slashes=False)
def c(text):
    """The view for the url routing to the /c<text> of the page

    return: html page with the text C and the text0
    underscore ryplaced with space
    """
    if "_" in text:
        li = text.split("_")
        text = " ".join(li)
    return "C {}".format(text)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
