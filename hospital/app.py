import os
import sqlite3

from datetime import datetime
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.serving import run_simple

from helpers import apology, login_required


# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Connect to database
conn = sqlite3.connect('hospital.db', check_same_thread=False)
db = conn.cursor()
db.execute("CREATE TABLE IF NOT EXISTS rooms (id INTEGER PRIMARY KEY, room_type TEXT, price INTEGER, status TEXT);")
db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, hash TEXT);")

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


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # If submitted via Post
    if request.method == "POST":
        # Get the username from the form
        username = request.form.get("username")
        usernames = db.execute("SELECT username FROM users;")

        # Check if the user name exists and not repeated
        if any(username in d.values() for d in usernames):
            return apology("Username already exists", 400)
        elif not username:
            return apology("Must provide a username", 400)

        # Get password from the form
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check if the passwords match and exist
        if password != confirmation:
            return apology("Password doesn't match", 400)
        elif not password or not confirmation:
            return apology("Must provide a password", 400)

        # Insert the user into users table
        hashed_password = generate_password_hash(password)
        db.execute(
            "INSERT INTO users(username, hash) VALUES(?, ?);", username, hashed_password
        )

        # Login the user
        rows = db.execute("SELECT id FROM users WHERE username = ?;", username)
        session["user_id"] = rows[0]["id"]
        return redirect("/")

    # If submitted via Get
    else:
        return render_template("register.html")


@app.route("/rooms")
def rooms():
    """ Return the page that contains the rooms info """
    return render_template("rooms.html")


@app.route("/single")
def single():
    """ Return the page that contains the single room info """
    availability = "available"
    cost = 2000
    #db.execute("INSERT INTO rooms(room_type, price, status) VALUES(?, ?, ?);", ("single", 2000, "available"))
    '''db.execute("UPDATE rooms SET status = ? WHERE room_type = 'single';", (availability,))
    db.execute("UPDATE rooms SET price = ? WHERE room_type = 'single';", cost)
    conn.commit()'''
    info = db.execute("SELECT price, status FROM rooms WHERE room_type = 'single';")
    result = info.fetchall()
    price = result[0][0]
    beds = result[0][1]
    return render_template("single.html", beds=beds, price=price)


@app.route("/double")
def double():
    """ Return the page that contains the double room info """
    availability = "available"
    cost = 1000
    #db.execute("INSERT INTO rooms(room_type, price, status) VALUES(?, ?, ?);", ("double", 1000, "available"))
    '''db.execute("UPDATE rooms SET status = ? WHERE room_type = 'double';", (availability,))
    db.execute("UPDATE rooms SET price = ? WHERE room_type = 'double';", (cost,))
    conn.commit()'''
    info = db.execute("SELECT price, status FROM rooms WHERE room_type = 'double';")
    result = info.fetchall()
    price = result[0][0]
    beds = result[0][1]
    return render_template("double.html", beds=beds, price=price)


@app.route("/multiple")
def multiple():
    """ Return the page that contains the multiple room info """
    availability = "available"
    cost = 500
    #db.execute("INSERT INTO rooms(room_type, price, status) VALUES(?, ?, ?);", ("multiple", 500, "available"))
    '''db.execute("UPDATE rooms SET status = ? WHERE room_type = 'multiple';", (availability,))
    db.execute("UPDATE rooms SET price = ? WHERE room_type = 'multiple';", (cost,))
    conn.commit()'''
    info = db.execute("SELECT price, status FROM rooms WHERE room_type = 'multiple';")
    result = info.fetchall()
    price = result[0][0]
    beds = result[0][1]
    return render_template("multiple.html", beds=beds, price=price)
    

@app.route("/devices")
def devices():
    """ Return the page that contains the Medical devices info """
    return render_template("devices.html")



# forgot password
 # user 
 # staff


# info
 # doctors
 # specialties
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

conn.commit()
conn.close()
# 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