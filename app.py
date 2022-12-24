from flask import Flask, flash, jsonify, redirect, render_template, request, session, send_file
from flask_session import Session
import sys

from flask_sqlalchemy import SQLAlchemy 
import logging

import random

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




@app.route("/BioVer", methods = ["POST", "GET"])
def BioVer(): 
    if request.method == "POST":
        verId = request.form.get("verifId")
        stat = request.form.get("check")
        
        if stat == "Yes":
            app.logger.info(stat + " Lesgoooo")
            app.logger.info(verId + " Lesgoooo")
            db.execute("UPDATE verifications SET BioStat='Approved' WHERE VerifId=:verId", verId=verId)
            ver= db.execute("SELECT * FROM verifications WHERE VerifId = :verId", verId=verId)
            db.execute("INSERT INTO accountstatus (accId, cardId, verifId, numTrips, expenditure, balance) VALUES (:acc, :card, :ver, 0, 0, 0)", acc=int(ver[0]["AccId"]), card=int(ver[0]["AccId"]) + 100, ver=int(ver[0]["VerifId"]))
            
            delDate = "2023-" + str(random.randint(1,12)) + "-" + str(random.randint(1,30))
            db.execute("INSERT INTO CardDelivery(AccId, DelDate, DelStat, VerifId) VALUES(:a, :date, 'Pending', :verId)", verId=int(verId), a=int(ver[0]["AccId"]), date=delDate)
    
    bios = db.execute("SELECT v.BioStat, v.BioDate, a.AccId, a.Name, a.Email, a.Gender, ua.NID, ua.DOB, v.VerifId FROM accounts a, userAccount ua, verifications v WHERE a.AccId = v.AccId AND ua.AccId = v.AccId AND v.BioStat <> 'Approved'")
    return render_template("bioVer.html", allReqs=bios)





@app.route("/VerifyUser", methods=["GET", "POST"])
def VerifyUser():
    if request.method == "POST":
        acc = request.form.get("userId")
        stat = request.form.get("check")
        db.execute("UPDATE userAccount SET IsVerified = :stat WHERE AccId = :accId", accId=acc, stat=stat)
        allReqs = db.execute('SELECT accounts.AccId,Name,Email,Gender,NID,DOB FROM accounts, userAccount WHERE accounts.AccId = userAccount.AccId AND userAccount.IsVerified = "Pending"')
        
        if stat == "YES":
            bioDate = "2023-" + str(random.randint(1,12)) + "-" + str(random.randint(1,30))
            db.execute("INSERT INTO verifications(AccId,  BioStat, BioDate) VALUES (:acc, 'Pending', :date)", acc=acc, date=bioDate)
            session["userVerif"] = "YES"
            
        
        return render_template("offUserVerf.html", allReqs=allReqs)

    else:
        allReqs = db.execute('SELECT accounts.AccId,Name,Email,Gender,NID,DOB FROM accounts, userAccount WHERE accounts.AccId = userAccount.AccId AND userAccount.IsVerified = "Pending"')
        return render_template("offUserVerf.html", allReqs=allReqs)






@app.route("/ConfirmBooking", methods = ["POST", "GET"])
def ConfirmBooking(trId=0):    
    if request.method == "POST":
        
        acc=session["user_id"]
        trId = request.form.get("tripId")
        stat = request.form.get("check")
        
        app.logger.info("yessssssssssssssss: " + stat)
        app.logger.info("yessssssssssssssss: " + trId)
        trInfo = db.execute("SELECT * FROM trip WHERE TripId=:tr", tr=trId)
        if stat == "Yes":
            db.execute("INSERT INTO booking(AccId, TripId) VALUES (:a, :t)", a=acc, t=trId)
            accStat = db.execute("SELECT * FROM accountStatus WHERE AccId=:a", a=acc)
            
            db.execute("UPDATE trip SET AvailSeat=:avSt WHERE TripId=:trId", avSt = int(trInfo[0]["Cost"]) -1, trId=trId)
            db.execute("UPDATE accountStatus SET NumTrips=:n, Expenditure=:exp, Balance=:b WHERE AccId=:acc", n=int(accStat[0]["NumTrips"])+1, exp=int(accStat[0]["Expenditure"])+int(trInfo[0]["Cost"]), b=int(accStat[0]["Balance"])-int(trInfo[0]["Cost"]), acc=acc)
        
        
    trInfo =db.execute("SELECT * FROM trip ")
    return render_template("booking.html", allReqs=trInfo)


@app.route("/Booking", methods = ["POST", "GET"])
def Booking():
    if request.method == "POST":
        trId = request.form.get("tripId")
        trInfo = db.execute("SELECT * FROM trip WHERE TripId=:tr", tr=trId)
        return render_template("BookingConfirmation.html", tr=trInfo[0])
        
    allReqs = db.execute("SELECT * FROM trip")    
    return render_template("booking.html", allReqs=allReqs)

    
    


@app.route("/deleteTrip", methods = ["POST", "GET"])
def deleteTrip():
    if request.method == "POST":
        trId = request.form.get("tripId")
        stat = request.form.get("check")
        app.logger.info(trId)
        if stat  == "Yes":
            db.execute("DELETE FROM trip WHERE TripId=:tId", tId=int(trId))
        
        
    allReqs = db.execute("SELECT * FROM trip")    
    return render_template("delTrip.html", allReqs=allReqs)





@app.route("/AccountStatus", methods = ["POST", "GET"])
def AccountStatus():  
    
    accStat = db.execute("SELECT * FROM accountStatus WHERE AccId = :acc",acc=session["user_id"])
    verifStat = db.execute("SELECT * FROM verifications WHERE AccId = :acc ", acc=session["user_id"])
    if accStat:
        cardId = accStat[0]["CardId"]
        accId = accStat[0]["AccId"]
        verifId = accStat[0]["VerifId"]
        numTrips = accStat[0]["NumTrips"]
        exp = accStat[0]["Expenditure"]
        bal = accStat[0]["Balance"]
    else:
        cardId = "Not Issued"
        accId = session["user_id"]
        verifId = "Not Applied"
        numTrips = "N/A"
        exp = "N/A"
        bal = "N/A"
    
    if verifStat:
        bioStat = verifStat[0]["BioStat"]
        bioDate = verifStat[0]["BioDate"]
    else:
        bioStat = "Not Requested"
        bioDate = "Not Requested"
        
    
    
    return render_template("AccountStatus.html", AccID=accId, CardId=cardId, VerifId=verifId, NumTrips=numTrips, Expenditure=exp, Balance=bal, bioStat=bioStat, bioDate=bioDate) 

@app.route("/Apply", methods = ["POST", "GET"])
def Apply():    
    if request.method == "POST":
        nid = request.form.get("verNid")
        dob = request.form.get("dob")
        
        db.execute("UPDATE userAccount SET NID=:nid, DOB=:dob, IsVerified='Pending' WHERE AccId = :acc", acc= session["user_id"], nid=nid, dob=dob)
        session["userVerif"] = "Pending"
        return render_template("landing.html")

    else:
        return render_template("apply.html")




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
        userVerif = db.execute("SELECT * from userAccount WHERE AccId = :accId", accId = session["user_id"])
        if not userVerif:
            session["userVerif"] = "No"
        else:
            session["userVerif"] = userVerif[0]["IsVerified"]
        # Redirect user to home page
        
        cardAvail = db.execute("SELECT * FROM verifications WHERE AccId = :accId", accId = session["user_id"])
        
        session["hasCard"] = "False"
        if cardAvail:
            if cardAvail[0]["BioStat"] == "Approved":
                session["hasCard"] = "True"
            
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
           
           
            db.execute("INSERT INTO accounts(Name, Email, Gender, Password, AccType) VALUES (:name, :email, :gender,  :password,  'User')", name=username, email=email, gender=gender, password=password)
            userIdNew = db.execute("SELECT * from accounts order by AccId DESC limit 1")
            
            
            
            db.execute("INSERT INTO phone(AccId, PhoneNumber) VALUES (:userID, :ph1)", userID=int(userIdNew[0]["AccId"]), ph1=phone1)
            
            if request.form.get("phone2"):
                phone2 = request.form.get("phone2")
                db.execute("INSERT INTO phone(AccId, PhoneNumber) VALUES (:userID, :ph2)", userID=int(userIdNew[0]["AccId"]), ph2=phone2)
            session["user_id"] = int(userIdNew[0]["AccId"])
            db.execute("INSERT INTO userAccount(AccId, NID, DOB, IsVerified) VALUES (:acc, 'NULL', 'NUL', 'No')", acc= session["user_id"])
    
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
    cardDel = db.execute("SELECT * from cardDelivery WHERE AccId = :accId", accId = session["user_id"])
        
    return render_template("Metrocard.html", delId = cardDel[0]["DeliveryId"], delTime =  cardDel[0]["DelDate"], delStat = cardDel[0]["DelStat"])








@app.route("/Transaction", methods=["GET", "POST"])
def Transaction():    
    if request.method == "POST":
        amount = request.form.get("Amount")
        date = request.form.get("Date")
    
        app.logger.info(amount)
        app.logger.info(date)
        app.logger.info(session["user_id"])
        app.logger.info(session["user_id"] + 100)
        db.execute("INSERT INTO transactions(AccId, CardId, Amount, Date) Values(:acc, :card, :amnt, :date)", acc=int(session["user_id"]),  card=int(session["user_id"]) + 100, amnt=amount, date=date)

        cardInfo = db.execute("SELECT * FROM accountStatus cardDelivery WHERE AccId = :accId", accId = session["user_id"])
        db.execute("UPDATE accountStatus SET Balance= :bal WHERE AccId = :acc", bal = int(amount) + int(cardInfo[0]["Balance"]), acc=int(session["user_id"]))
        return render_template("landing.html")
    else:
        return render_template("Transaction.html")








@app.route("/TripsAndBooking", methods=["GET", "POST"])
def tripsNbooking(warning = 0):
    app.logger.info("Logging: ")
    app.logger.info(request.method)
    if request.method == "POST":
        
        # Store the user input
        trainName = request.form.get("trainName")
        date = request.form.get("date")
        stTime = request.form.get("stTime")
        dest = request.form.get("dest")
        totSeat = request.form.get("totSeat")
        AvailSeat = totSeat
        cost = request.form.get("cost")

            

        app.logger.info("Logging: ")
        app.logger.info(trainName)
        app.logger.info(date)
        app.logger.info(stTime)
        app.logger.info(dest)
        app.logger.info(totSeat)
        app.logger.info(AvailSeat)
        app.logger.info(cost)
        db.execute("INSERT INTO trip(TrainName, Date, TripTime, Dest, AvailSeat, TotalSeat, Cost) Values(:trainName, :date, :tripTime, :dest, :availSeat, :totSeat, :cost)", trainName=trainName, date=date, tripTime=stTime, dest=dest, availSeat=AvailSeat, totSeat=totSeat, cost=cost)


        return render_template("tripsNbooking.html", warning = 2)

    else:   
        return render_template("tripsNbooking.html", warning = 0)