#!/usr/bin/python3
"""
Start the flask application server listening on 0.0.0.0, port 5000
and display 'Hello HBNB!' on /
and display 'HBNB' on /hbnb
and display C followed by a variable passed to the route /c/<vaiable>
and display Python follwed by a variable paased to the route /poython/<text>
and display <n> is a number only if n is a number
and display <n> is even or odd only if n is a number
"""

from flask import Flask, redirect, url_for, render_template

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


@app.route("/python", defaults={"text": "is cool"}, strict_slashes=False)
def python_default(text):
    """The view for the url that redirect to the url rull /python<text>
    with th default of text being = is cool if it's empty

    """
    return redirect(url_for("python", text=text))


@app.route("/python/<text>", strict_slashes=False)
def python(text):
    """The view for the url routing to the /python<text> of the page

    return: html page with the text python and the text
    underscore ryplaced with space

    """
    if "_" in text:
        li = text.split("_")
        text = " ".join(li)
    return "Python {}".format(text)


@app.route("/number/<int:n>")
def is_number(n):
    """/number/<n> routing rull display “n is a number”
    only if n is an integer"""

    return f'{n} is a number'


@app.route("/number_template/<int:n>", strict_slashes=False)
def render_html_number(n):
    return render_template("5-number.html", number=n)


@app.route("/number_odd_or_even/<int:n>", strict_slashes=False)
def render_html_even_odd(n):
    return render_template("6-number_odd_or_even.html", number=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
