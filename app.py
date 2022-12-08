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
def index():
    return render_template("layout.html")