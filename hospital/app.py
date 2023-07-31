import os
import sqlite3

from datetime import datetime
from flask import flash, Flask, redirect, render_template, request, session
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
db.execute("CREATE TABLE IF NOT EXISTS rooms (id INTEGER PRIMARY KEY, room_type TEXT, price INTEGER, status TEXT);")
db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, hash TEXT);")
db.execute("CREATE TABLE IF NOT EXISTS info (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, first_name TEXT, last_name TEXT, email TEXT, phone TEXT, age INTEGER, user_id INTEGER, FOREIGN KEY (user_id) REFERENCES users(id));")
db.execute("CREATE INDEX IF NOT EXISTS username ON users (username);")

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


@app.route("/about")
def about():
    """ Return the page that contains the about info """
    return render_template("about.html")


@app.route("/appointment")
def appointment():
    """Schedule an appointment"""
    # if has a medical card
        # price and payment options
    # else
        # price and payment options
    return "This is the appointment page"


@app.route("/cancer")
def cancer():
    """ Return the page that contains the cancer treatment info """
    return render_template("cancer.html")


@app.route("/devices")
def devices():
    """ Return the page that contains the Medical devices info """
    return render_template("devices.html")


@app.route("/double")
def double():
    """ Return the page that contains the double room info """
    availability = "available"
    cost = 1000
    
    # The following code can be used to insert/update the data into the database if needed
    '''db.execute("INSERT INTO rooms(room_type, price, status) VALUES(?, ?, ?);", ("double", 1000, "available"))
    db.execute("UPDATE rooms SET status = ? WHERE room_type = 'double';", (availability,))
    db.execute("UPDATE rooms SET price = ? WHERE room_type = 'double';", (cost,))
    conn.commit()'''
    
    result = db.execute("SELECT price, status FROM rooms WHERE room_type = 'double';").fetchall()
    price = result[0][0]
    beds = result[0][1]
    return render_template("double.html", beds=beds, price=price)


@app.route("/forgot", method=["GET", "POST"])
def forgot():
    """ Change the password if the user forgot it """
    return "This is the forgot password page"
    
@app.route("/multiple")
def multiple():
    """ Return the page that contains the multiple room info """
    availability = "available"
    cost = 500
    
    # The following code can be used to insert/update the data into the database if needed
    '''db.execute("INSERT INTO rooms(room_type, price, status) VALUES(?, ?, ?);", ("multiple", 500, "available"))
    db.execute("UPDATE rooms SET status = ? WHERE room_type = 'multiple';", (availability,))
    db.execute("UPDATE rooms SET price = ? WHERE room_type = 'multiple';", (cost,))
    conn.commit()'''
    
    result = db.execute("SELECT price, status FROM rooms WHERE room_type = 'multiple';").fetchall()
    price = result[0][0]
    beds = result[0][1]
    return render_template("multiple.html", beds=beds, price=price)
    

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Must provide username")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("Must provide password")
            return render_template("login.html")

        # Query database for username
        username = request.form.get("username")
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?;", (username,)
        ).fetchall()
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0][2], request.form.get("password")
        ):
            flash("Invalid username and/or password")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0][0]

        # Redirect user to home page
        return redirect("/profile")

    # User reached route via GET 
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
        usernames = db.execute("SELECT username FROM users;").fetchall()
        usernames = [dict(username=row[0]) for row in usernames]

        # Check if the username exists and is not repeated 
        if any(username in d.values() for d in usernames):
            flash("Username already exists")
            return redirect("/register")
        elif not username:
            flash("Must provide a username")
            return redirect("/register")

        # Get password from the form
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check if the passwords match and exist
        if password != confirmation:
            flash("Password doesn't match")
            return redirect("/register")
        elif not password or not confirmation:
            flash("Must provide a password")
            return redirect("/register")
        
        # Insert the user into users table
        hashed_password = generate_password_hash(password)
        db.execute("BEGIN TRANSACTION;")
        db.execute(
            "INSERT INTO users(username, hash) VALUES(?, ?);", (username, hashed_password)
        )
        db.execute("COMMIT;")
        conn.commit()   
        
        rows = db.execute("SELECT id FROM users WHERE username = ?;", (username,)).fetchall() 
        session["user_id"] = rows[0][0]
        ID = session["user_id"]
        
        # Get the user info from the form
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        age = request.form.get("age")
        phone = request.form.get("phone_number")
        email = request.form.get("email")
        
        # Insert the user info into info table
        db.execute("INSERT INTO info(first_name, last_name, age, phone, email, user_id) VALUES(?, ?, ?, ?, ?, ?);", (first_name, last_name, age, phone, email, ID))
        db.execute("COMMIT;")
        conn.commit()
        
        # Login the user
        return redirect("/profile")

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
    
    # The following code can be used to insert/update the data into the database if needed
    '''db.execute("INSERT INTO rooms(room_type, price, status) VALUES(?, ?, ?);", ("single", 2000, "available"))
    db.execute("UPDATE rooms SET status = ? WHERE room_type = 'single';", (availability,))
    db.execute("UPDATE rooms SET price = ? WHERE room_type = 'single';", cost)
    conn.commit()'''
    
    result = db.execute("SELECT price, status FROM rooms WHERE room_type = 'single';").fetchall()
    price = result[0][0]
    beds = result[0][1]
    return render_template("single.html", beds=beds, price=price)


@app.route("/services")
def services():
    """ Return the page that contains the services info """
    return render_template("services.html")


# forgot password
 # user 
 # staff

# pay for medical card if it doesn't exist
 # schedule appointment

# maps / dxns
 # room maps
 # hospital map on google maps


if __name__ == '__main__':
    app.run(debug=True)

conn.commit()
conn.close()
# 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