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
db = SQL("sqlite:///database.db")

# Setting up the flask environment
app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

#app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:password123@localhost/metroraileticket.sql"
#db = SQLAlchemy(app)





Session(app)

RegOrLogin = 0

app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/")
@app.route("/Home")
def index():    
    return render_template("landing.html", rows=[])

@app.route("/AboutUs")
def AboutUs():
    return render_template("AboutUs.html")

@app.route("/Complaints", methods = ["POST", "GET"])
def Complaints():
    if request.method == "POST":
        # Verify that the input fields are not empty
        if not request.form.get("subject"):
            return render_template("Complaints.html", submission=True, warning = 1)
        if not request.form.get("description"):
                return render_template("Complaints.html", submission=True, warning = 1)
        
        compSub = request.form.get("subject")
        compDesc = request.form.get("description")
        
        print(session["user_id"], file=sys.stderr)
        db.execute("INSERT INTO complaint (AccId, ComplaintText, ComplaintSubj) VALUES (:userID, :desc, :sub)", userID=int(session["user_id"]), desc = compDesc, sub = compSub)
        
        return render_template("Complaints.html", submission=True, warning = 0)
    else:
        return render_template("Complaints.html", submission=False, warning = 0)
    

@app.route("/FAQ")
def FAQ():
    faqList = db.execute("SELECT * FROM faqList")
    return render_template("FAQ.html", faqList=faqList)






@app.route("/Login", methods=["GET", "POST"])
def login(warning = 0):
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
        rows = db.execute("SELECT * FROM accounts WHERE Name = :username", username=username)

        # Ensure the user exists and their password is correct
        if len(rows) != 1 or not rows[0]["Password"] == password:
            return render_template("Login.html",warning = 1)

        # Hold the user's session
        session["user_id"] = int(rows[0]["AccId"])
        session["accType"] = (rows[0]["AccType"])

        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("Login.html", warning=0)





@app.route("/SignUp", methods=["GET", "POST"])
def SignUp(warning = 0):
    if request.method == "POST":
            # Verify that the input fields are not empty
            if not request.form.get("signupUser"):
                return render_template("Signup.html", warning = 1)
            if not request.form.get("check"):
                return render_template("Signup.html",warning = 1)
            if not request.form.get("signupPassword"):
                return render_template("Signup.html",warning = 1)
            if not request.form.get("signupEmail"):
                return render_template("Signup.html",warning = 1)
            if not request.form.get("phone1"):
                return render_template("Signup.html",warning = 1)
            
            
            # Store the user input
            username = request.form.get("signupUser")
            email = request.form.get("signupEmail")
            password =  request.form.get("signupPassword")
            gender = request.form.get("check")
            phone1 = request.form.get("phone1")
            
                
            app.logger.info("name = " + username)
            app.logger.info("gender = " + gender)
            app.logger.info("ph1 = " + phone1)
           # app.logger.info("ph2 = " + phone2)
           
            db.execute("ALTER TABLE accounts AUTO_INCREMENT = (SELECT MAX( 'AccId' ) FROM acccounts ;)")
           
           
            db.execute("INSERT INTO accounts(Name, Email, Gender, Password, AccType) VALUES (:name, :email, :gender,  :password,  'User')", name=username, email=email, gender=gender, password=password)
            userIdNew = db.execute("SELECT * from accounts order by AccId DESC limit 1")
            
            
            
            db.execute("INSERT INTO phone(AccId, PhoneNumber) VALUES (:userID, :ph1)", userID=int(userIdNew[0]["AccId"]), ph1=phone1)
            
            if request.form.get("phone2"):
                phone2 = request.form.get("phone2")
                db.execute("INSERT INTO phone(AccId, PhoneNumber) VALUES (:userID, :ph2)", userID=int(userIdNew[0]["AccId"]), ph2=phone2)
            
            return render_template("Login.html", warning = 0)

    else:   
        return render_template("Signup.html", warning = 0)












@app.route("/Logout")
def logout():
    # Clear the current session to log the user out, and redirect them to the homepage
    session.clear()
    return redirect("/")











@app.route("/Metrocard")
def metrocard():
    return render_template("Metrocard.html")



@app.route("/Transaction")
def Transaction():
    return render_template("Transaction.html")

@app.route("/TripsAndBooking")
def tripsNbooking():
    return render_template("tripsNbooking.html")