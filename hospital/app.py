import os
import sqlite3


from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

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
@login_required
def index():
    """Home page"""
    if request.method == "POST":
        
        return redirect("/homepage")
    
    return render_template("homepage.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    
    
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register the user"""
   
    
@app.route("/homepage")
def homepage():
    """Display the homepage"""