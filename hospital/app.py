import os
import sqlite3

from datetime import datetime
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.serving import run_simple

from helpers import login_required


# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Connect to database
conn = sqlite3.connect('hospital.db', check_same_thread=False)
db = conn.cursor()


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    """Home page"""
    return render_template("homepage.html")


@app.route("/appointment")
def appointment():
    """Schedule an appointment"""
    # if has a medical card
        # price and payment options
    # else
        # price and payment options
    return "This is the appointment page"


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM hospital WHERE username = ?;", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/Profile")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/physicians")
def physicians():
    """ Return the page that contains the physicians info """
    name = request.args.get('name')
    if name:
        return render_template(name + '.html')
    return render_template("physicians.html")


# fogot password
# register
 # user 
 # staff

# logout

# info
 # doctors
 # specialites
 # machines and their status 

# schedule appointment

# number of beds 
 # the price 
 # standard

# pay for medical card if it doesn't exist
 # schedule appointment

# maps / dxns
 # room maps
 # hospital map on google maps

# for staff work schedule

if __name__ == '__main__':
    app.run(debug=True)
# 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