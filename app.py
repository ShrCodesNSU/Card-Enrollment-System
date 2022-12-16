from flask import Flask, flash, jsonify, redirect, render_template, request, session, send_file
from flask_session import Session
import sys

from flask_sqlalchemy import SQLAlchemy 
import logging

import sqlite3, os, time, fnmatch
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL
from datetime import date 

# Initializing the database
db = SQL("sqlite:///metroRail.db")

# Setting up the flask environment
app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

#app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/metroraileticket.sql"
#db = SQLAlchemy(app)





Session(app)

RegOrLogin = 0

app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/")
@app.route("/Home")
def index():
    
    rows = db.execute("SELECT * FROM accounts WHERE Username = :username", username="Daniel K. Pemberton")
    return render_template("landing.html", rows=rows)

@app.route("/AboutUs")
def AboutUs():
    return render_template("AboutUs.html")

@app.route("/Complaints")
def Complaints():
    return render_template("Complaints.html")

@app.route("/FAQ")
def FAQ():
    return render_template("FAQ.html")






@app.route("/Login", methods=["GET", "POST"])
def login(warning = 0):
    print(request.method, file=sys.stderr)
    if request.method == "POST":
        # Verify that the input fields are not empty
        if not request.form.get("loginUser"):
            return render_template("Login.html", warning = 1)
        if not request.form.get("loginPassword"):
            return render_template("Login.html",warning = 1)
        
        # Store the user input
        username = request.form.get("loginUser")
        password = request.form.get("loginPassword")
        

        # Query the database for user credentials
        rows = db.execute("SELECT * FROM accounts WHERE Username = :username", username=username)

        # Ensure the user exists and their password is correct
        if len(rows) != 1 or not rows[0]["Password1"] == password:
            return render_template("Login.html",warning = 1)

        # Hold the user's session
        session["user_id"] = rows[0]["accId"]

        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("Login.html", warning=0)


@app.route("/Logout")
def logout():
    # Clear the current session to log the user out, and redirect them to the homepage
    session.clear()
    return redirect("/")











@app.route("/Metrocard")
def metrocard():
    return render_template("Metrocard.html")

@app.route("/SignUp")
def SignUp():
    return render_template("Signup.html")


@app.route("/Transaction")
def Transaction():
    return render_template("Transaction.html")

@app.route("/TripsAndBooking")
def tripsNbooking():
    return render_template("tripsNbooking.html")