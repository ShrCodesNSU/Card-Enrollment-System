from flask import Flask, flash, jsonify, redirect, render_template, request, session, send_file
from flask_session import Session
import sqlite3, os, time, fnmatch
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL
from datetime import date

# Initializing the database
#db = SQL("sqlite:///data.db")

# Setting up the flask environment
app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

RegOrLogin = 0

app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/")
@app.route("/Home")
def index():
    return render_template("landing.html")

@app.route("/AboutUs")
def AboutUs():
    return render_template("AboutUs.html")

@app.route("/Complaints")
def Complaints():
    return render_template("Complaints.html")

@app.route("/FAQ")
def FAQ():
    return render_template("FAQ.html")

@app.route("/Login")
def login():
    return render_template("Login.html")

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