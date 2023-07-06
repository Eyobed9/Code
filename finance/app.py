import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Create a variable that selects all the necessary table elements
    id = session.get("user_id")

    table = db.execute(
        "SELECT name, price, shares, shares * price as total FROM purchase WHERE user_id = ? GROUP BY name;",
        id,
    )

    # Calculate cash and total
    cash = db.execute("SELECT cash FROM users WHERE id = ?;", id)
    cash = cash[0]["cash"]

    Total = 0
    for row in table:
        Total += row["total"]
    total = cash + Total

    return render_template("index.html", table=table, cash=cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # If submitted via Post
    if request.method == "POST":
        # look for the symbol
        time = datetime.now()
        symbol = request.form.get("symbol").upper()
        lookUp = lookup(symbol)

        # Check if the symbol exists and correct
        if not symbol:
            return apology("Missing symbol", 400)
        elif lookUp == None:
            return apology("Invalid symbol", 400)

        # Check shares for errors
        shares = request.form.get("shares")

        try:
            shares = int(shares)
        except ValueError:
            return apology("Invalid shares", 400)

        # If the user inputted a positive integer
        if shares < 1:
            return apology("Input a positive integer", 400)

        # look up the stocks current price
        price = lookUp["price"]
        # Calculate the total amount
        total = price * shares
        symbol = symbol.upper()
        # Begin transaction
        db.execute("BEGIN TRANSACTION")
        # Check the amount of cash the user have
        id = session.get("user_id")
        money = db.execute("SELECT cash FROM users WHERE id = ?;", id)
        cash = money[0]["cash"]

        # if insufficient funds
        if cash < total:
            return apology("Insufficient funds", 400)
        # if sufficient
        else:
            cash -= total
            db.execute("UPDATE users SET cash = ? WHERE id = ?;", cash, id)

        # Create tables if don't exist
        db.execute(
            "CREATE TABLE IF NOT EXISTS purchase (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id INT, price REAL NOT NULL, name TEXT NOT NULL, shares INT, time NUMERIC NOT NULL, FOREIGN KEY (user_id) REFERENCES users(id));"
        )
        db.execute(
            "CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, user_id INT, price REAL NOT NULL, name TEXT NOT NULL, shares INT, time NUMERIC NOT NULL, FOREIGN KEY (user_id) REFERENCES users(id));"
        )

        # Insert to table buy
        db.execute(
            "INSERT INTO history (user_id, price, time, name, shares) VALUES (?, ?, ?, ?, ?);",
            id,
            price,
            time,
            symbol,
            shares,
        )

        # Insert to table purchase
        symbols = db.execute(
            "SELECT DISTINCT(name) FROM purchase WHERE user_id = ?;", id
        )
        if not any(symbol in d.values() for d in symbols):
            db.execute(
                "INSERT INTO purchase (user_id, price, time, name, shares) VALUES (?, ?, ?, ?, ?);",
                id,
                price,
                time,
                symbol,
                shares,
            )
        else:
            db.execute(
                "UPDATE purchase SET shares = shares + ? WHERE user_id = ? AND name = ?;",
                shares,
                id,
                symbol,
            )

        db.execute("COMMIT")

        # Go to the homepage
        return redirect("/")

    # If submitted via Get
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    id = session["user_id"]
    history = db.execute(
        "SELECT name, shares, price, time FROM history WHERE user_id = ? ORDER BY time DESC;",
        id,
    )
    return render_template("history.html", history=history)


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
            "SELECT * FROM users WHERE username = ?;", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # If submitted via Post
    if request.method == "POST":
        symbol = request.form.get("symbol")
        quote = lookup(symbol)

        # If the user didn't provide an input
        if not symbol:
            return apology("Missing symbol", 400)
        # If the symbol is invalid
        elif quote == None:
            return apology("Invalid symbol", 400)
        # If the input is valid
        return render_template("quoted.html", quotes=quote)

    # If submitted via Get
    else:
        return render_template("quote.html")


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


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # Get the id of the user and symbols
    id = session.get("user_id")
    symbols = db.execute("SELECT DISTINCT(name) FROM purchase WHERE user_id = ?;", id)

    # If the user request via Post
    if request.method == "POST":
        # Get the symbol from the form and time
        time = datetime.now()
        symbol = request.form.get("symbol")

        # Check the symbol for errors
        if not symbol:
            return apology("Must provide a stock", 400)

        look = lookup(symbol)
        if look == None:
            return apology("Invalid stock", 400)
        elif not any(symbol in d.values() for d in symbols):
            return apology("Access denied", 400)

        # Get shares from the form
        shares = request.form.get("shares")

        # Change shares to integer and check if its positive
        try:
            shares = int(shares)
        except ValueError:
            return apology("Invalid shares", 400)

        if shares < 1:
            return apology("Input a positive integer", 400)

        # Check if the user didn't ask for shares more than he/she has
        share = db.execute(
            "SELECT shares FROM purchase WHERE user_id = ? AND name = ?;", id, symbol
        )
        share = share[0]["shares"]

        Shares = -shares
        price = look["price"]
        symbol = symbol.upper()

        if shares > share:
            return apology("Enter valid number of shares", 400)

        # Create table sell if not exist and insert values
        db.execute("BEGIN TRANSACTION")
        db.execute(
            "INSERT INTO history (user_id, price, time, name, shares) VALUES (?, ?, ?, ?, ?);",
            id,
            price,
            time,
            symbol,
            Shares,
        )

        # Complete the transaction
        cash = db.execute("SELECT cash FROM users WHERE id = ?;", id)
        cash = cash[0]["cash"]
        cash += price * shares

        # if the user want to sell all
        if shares == share:
            db.execute(
                "DELETE FROM purchase WHERE user_id = ? AND name = ?;", id, symbol
            )
        # if the user want to sell some
        else:
            db.execute(
                "UPDATE purchase SET shares = shares - ? WHERE user_id = ? AND name = ?;",
                shares,
                id,
                symbol,
            )

        db.execute("UPDATE users SET cash = ? WHERE id = ?;", cash, id)

        db.execute("COMMIT")

        return redirect("/")

    # If the user request via Get
    else:
        # Get the available stocks from the table
        return render_template("sell.html", symbols=symbols)


@app.route("/changePassword", methods=["GET", "POST"])
@login_required
def changePassword():
    """Change the old password"""

    # Get the user's id
    id = session.get("user_id")

    # if the user request via post
    if request.method == "POST":
        old = request.form.get("old")
        new = request.form.get("new")
        confirm = request.form.get("confirm")

        if not old or not new or not confirm:
            return apology("Must fill all fields", 400)
        if new != confirm:
            return apology("Password doesn't match", 400)


        # Ensure the old password is correct
        row = db.execute("SELECT hash FROM users WHERE id = ?;", id)
        if not check_password_hash(row[0]["hash"], old):
            return apology("Invalid password", 400)
        hash = generate_password_hash(new)
        db.execute("UPDATE users SET hash = ? WHERE id = ?;", hash, id)

        # Redirect the user to the home page
        return redirect("/")

    # If the user request via get
    else:
        return render_template("change_password.html")
