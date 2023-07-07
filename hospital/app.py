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
# login
 # user
 # staff

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
