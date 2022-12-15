from flask import Flask, flash, jsonify, redirect, render_template, request, session, send_file
from flask_session import Session
import sqlite3, os, time, fnmatch
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL
from datetime import date

# Initializing the database
db = SQL("sqlite:///data.db")

# Setting up the flask environment
app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

RegOrLogin = 0

app.config["TEMPLATES_AUTO_RELOAD"] = True

# Registration
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Verify that the input fields are not empty
        if not request.form.get("username"):
            return render_template("reg-login.html", reg=0, warning=1, warningType=1)
        if not request.form.get("password"):
            return render_template("reg-login.html", reg=0, warning=1, warningType=2)
        if not request.form.get("confirm"):
            return render_template("reg-login.html", reg=0, warning=1, warningType=3)

        # Record the user input
        username = request.form.get("username")
        password = (request.form.get("password"))
        confirm = (request.form.get("confirm"))

        # Verify that a user with the same username does not exist.
        userCheck =  db.execute("SELECT * FROM user WHERE name=:name", name=username)
        if userCheck:
            return render_template("reg-login.html", reg=0, warning=1, warningType=400)

        # Check if passwords don't match
        if password != confirm:
            return render_template("reg-login.html", reg=0, warning=1, warningType=4)
        
        # Generate a password hash
        hashPass = generate_password_hash(password)

        # Store the data in the SQL database
        with sqlite3.connect("data.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO user (name, hash) VALUES (?, ?)", (username, hashPass))
            con.commit()
        
        # Return the user to the index page.
        return render_template("index.html", success=1)
    else:
        # If the requested method is not POST, the user is just tryig to access the registration page
        RegOrLogin = 0
        return render_template("reg-login.html", reg = RegOrLogin)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Verify that the input fields are not empty
        if not request.form.get("username"):
            return render_template("reg-login.html", reg = 1, warning = 1, warningType=1)
        if not request.form.get("password"):
            return render_template("reg-login.html", reg = 1, warning = 1, warningType=2)
        
        # Store the user input
        username = request.form.get("username")
        password = request.form.get("password")

        # Query the database for user credentials
        rows = db.execute("SELECT * FROM user WHERE name = :username", username=username)

        # Ensure the user exists and their password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return render_template("reg-login.html", reg = 1, warning = 1, warningType=5)

        # Hold the user's session
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")
    else:
        # If the requested method is not POST, the user is just tryig to access the registration page
        RegOrLogin = 1
        return render_template("reg-login.html", reg = RegOrLogin)

@app.route("/logout")
def logout():
    # Clear the current session to log the user out, and redirect them to the homepage
    session.clear()
    return redirect("/")

@app.route("/")
def index():
    # Render the index.html page
    return render_template("index.html")

@app.route("/bookshelf")
def bookshelf():

    history = []
    
    # Query database for the books the user has bought
    tmp = db.execute("SELECT * FROM history WHERE userID=:userID", userID = session["user_id"])
    if tmp:
        for row in tmp:
    
            # Query the database for details of the books above
            history.append(db.execute("SELECT * FROM products WHERE id=:id", id=row["bookID"]))
    
    # Return the render template
    return render_template("bookshelf.html", data=history)


# Collections page
@app.route("/collections")
def collections():
    data = []

    # If the user is not logged in, show them the entire library
    if not session:
        data = db.execute("SELECT * FROM products")
        return render_template("collections.html", tmp=data, search=1)

    # otherwise show them all the books except the ones they have bought already
    else:
        tmp = db.execute("SELECT id FROM products EXCEPT SELECT bookID FROM history WHERE userID=:id", id=session["user_id"])
        for rows in tmp:
            data.append(db.execute("SELECT * FROM products WHERE id=:id", id=rows["id"]))
        return render_template("collections.html", tmp=data, search=1, list=1)

# Account details page
@app.route("/account")
def account():
    # Get the user's data and transaction history
    data = db.execute("SELECT * FROM user WHERE id=:id", id=session["user_id"])
    history = db.execute("SELECT * FROM userHistory WHERE userID=:id", id=session["user_id"])

    # Count the total number of books they own
    total = 0
    for rows in history:
        total += 1

    # Return the account page
    return render_template("account.html", data=data[0], total=total, history=history)

@app.route("/cash", methods=["POST"])
def cash():
    # Get the user's data and transaction history (to render the account.html afterwards)
    data = db.execute("SELECT * FROM user WHERE id=:id", id=session["user_id"])
    history = db.execute("SELECT * FROM userHistory WHERE userID=:id", id=session["user_id"])

    # Count the total number of books owned (same reason as above)
    total = 0
    for rows in history:
        total += 1

    # Check the inputs are not empty
    if not request.form.get("card"):
        return render_template("account.html", data=data[0], total=total, history=history, warning=1, warningType=1)
    if not request.form.get("amount"):
        return render_template("account.html", data=data[0], total=total, history=history, warning=1, warningType=2)
    else:
        # Check that the inputs are digits only
        cardNo = request.form.get("card")
        for char in cardNo:
            if not char.isdigit():
                return render_template("account.html", data=data[0], total=total, history=history, warning=1, warningType=5)
        amount = request.form.get("amount")
        for char in amount:
            if not char.isdigit():
                return render_template("account.html", data=data[0], total=total, history=history, warning=1, warningType=5)
        amount = float(amount)
        cashNew = 0

        # Verify that the card is valid and that the amount is within 10000 to prevent spam
        if len(cardNo) != 16:
            return render_template("account.html", data=data[0], total=total, history=history, warning=1, warningType=3)
        if amount < 0 or amount > 10000:
            return render_template("account.html", data=data[0], total=total, history=history, warning=1, warningType=4)
        else:
            # Update the user's cash and redirect them to the account page
            cash = db.execute("SELECT * FROM user WHERE id=:id", id=session["user_id"])
            cashNew += cash[0]["credits"] + amount
            db.execute("UPDATE user SET credits=:credits", credits=cashNew)
            return redirect("/account")

# Wishlist
@app.route("/cart", methods=["GET", "POST"])
def cart():
    if request.method == "POST":
        # Check if the user has requested to remove the book from the wishlist
        if request.form.get("remove"):
            db.execute("DELETE FROM cart WHERE (userID=:userID AND bookID=:bookID)", userID=session["user_id"], bookID=request.form.get("remove"))
            row = db.execute("SELECT * FROM cart WHERE (userID=:userID)", userID=session["user_id"])

            # Show the updated page
            return render_template("cart.html", data=row)
    
    # If the requested method is not POST, the user is just trying to access the registration page
    else:
        row = db.execute("SELECT * FROM cart WHERE userID=:userID", userID=session["user_id"])
        return render_template("cart.html", data=row)

# The product page
@app.route("/productPage", methods=["POST"])
def productPage():

    # Get the book's ID number
    bookID = request.form.get("bookID")

    # Get the book's details
    tmp = db.execute("SELECT * FROM products WHERE id=:id", id=bookID)

    # Read the book's description
    with open("." + tmp[0]["path"] + "/description.txt", 'r') as file:
        description = file.read().replace('\n', '') 

    # Render the page
    return render_template("productPage.html", data=tmp, description=description)

# Book return page
@app.route("/return", methods=["POST"])
def returnBook():

    # Get the book's ID and details
    bookID = int(request.form.get("return"))
    data = db.execute("SELECT * FROM products WHERE id=:bookID",bookID=bookID)

    # Render the page
    return render_template("return.html", bookID=bookID, data=data, path=data[0]["path"])

# Confirm the return of book
@app.route("/returnConfirm", methods=["POST"])
def returnConfirm():
    # Get the book ID, user's information, user's transaction history, the book's details.
    bookID = request.form.get("return")
    userData = db.execute("SELECT * FROM user WHERE id=:id", id=session["user_id"])
    bookHistoryData = db.execute("SELECT * FROM history WHERE (bookID=:bookID AND userID=:id)", bookID=bookID, id=session["user_id"])
    bookData=db.execute("SELECT * FROM products WHERE (id=:bookID)", bookID=bookID)

    # calculate the amount that will be returned to the user.
    cash = float(userData[0]["credits"]) + (0.8 * float(bookHistoryData[0]["paid"]))
    
    # Remove the book from the user's bookshelf
    db.execute("DELETE FROM history WHERE (bookID=:bookID AND userID=:userID)", bookID=bookID, userID=session["user_id"])

    # add the transaction to the transaction history
    db.execute("INSERT INTO userHistory (userID, bookID, bookName, paid, date) VALUES (:userID, :bookID, :bookName, :paid, :date)", userID=session["user_id"], bookID=bookID, bookName=bookData[0]["name"], paid=-(0.8 * (bookData[0]["price"])), date=date.today())

    # Update the amount of credits the user has after refund
    db.execute("UPDATE user SET credits=:credits WHERE id=:userID", credits=cash, userID=session["user_id"])

    # Redirect the user to homepage
    return redirect("/")

# Display the details of a book after the user has purchased it
@app.route("/boughtProductPage", methods=["POST"])
def boughtProductPage():
    tmp = 0
    data = []
    # Check that bookID exists
    if not request.form.get("bookID"):
        tmp = tmp
    else:
        # Store the bookID
        tmp = int(request.form.get("bookID"))
        # Get book data
        data = db.execute("SELECT * FROM products WHERE id=:id", id=tmp)
        # update averaage review
        avgReview = updateRating(tmp)
        # Read the file description   
        with open("." + data[0]["path"] + "/description.txt", 'r') as file:
            description = file.read().replace('\n', '')
        # Render the site
        return render_template("boughtProductPage.html", data = data, description=description, avgReview=avgReview, review=1)
    if not request.form.get("hate"):
        tmp = tmp
    
    # Check the type of review: hate, ok, love
    else:
        # Get the book's ID
        tmp = int(request.form.get("hate"))
        # Get the reviews of the user for that book
        review = db.execute("SELECT * FROM reviews WHERE userID=:userID AND bookID=:bookID", userID = session["user_id"], bookID=tmp)
        
        # IF there are no reviews of the user for that book, insert the review
        if not review:
            db.execute("INSERT INTO reviews (userID, bookID, review) VALUES (:userID, :bookID, :review)", userID=session["user_id"], bookID=tmp, review=1)
        # Else update their review
        else:
            db.execute("UPDATE reviews SET review=:review WHERE (userID=:userID AND bookID=:bookID)", review=1, userID=session["user_id"], bookID=tmp)
        
        data = db.execute("SELECT * FROM products WHERE id=:id", id=tmp)
        # Update the current review after averaging everyone else's review
        avgReview = updateRating(tmp)   
        with open("." + data[0]["path"] + "/description.txt", 'r') as file:
            description = file.read().replace('\n', '') 

        # Render the page
        return render_template("boughtProductPage.html", data = data, description=description, avgReview=avgReview, review=1)
    if not request.form.get("ok"):
        tmp = tmp
    else:
        tmp = int(request.form.get("ok"))
        review = db.execute("SELECT * FROM reviews WHERE userID=:userID AND bookID=:bookID", userID = session["user_id"], bookID=tmp)
        
        if not review:
            db.execute("INSERT INTO reviews (userID, bookID, review) VALUES (:userID, :bookID, :review)", userID=session["user_id"], bookID=tmp, review=3)
        else:
            db.execute("UPDATE reviews SET review=:review WHERE (userID=:userID AND bookID=:bookID)", review=3, userID=session["user_id"], bookID=tmp)
        
        data = db.execute("SELECT * FROM products WHERE id=:id", id=tmp)
        avgReview = updateRating(tmp)   
        with open("." + data[0]["path"] + "/description.txt", 'r') as file:
            description = file.read().replace('\n', '') 
        return render_template("boughtProductPage.html", data = data, description=description, avgReview=avgReview, review=1)
    if not request.form.get("like"):
        tmp = tmp
    
    else:
        tmp = int(request.form.get("like"))
        review = db.execute("SELECT * FROM reviews WHERE userID=:userID AND bookID=:bookID", userID = session["user_id"], bookID=tmp)
        
        if not review:
            db.execute("INSERT INTO reviews (userID, bookID, review) VALUES (:userID, :bookID, :review)", userID=session["user_id"], bookID=tmp, review=5)
        else:
            db.execute("UPDATE reviews SET review=:review WHERE (userID=:userID AND bookID=:bookID)", review=5, userID=session["user_id"], bookID=tmp)
        
        data = db.execute("SELECT * FROM products WHERE id=:id", id=tmp)
        avgReview = updateRating(tmp)   
        with open("." + data[0]["path"] + "/description.txt", 'r') as file:
            description = file.read().replace('\n', '') 
        return render_template("boughtProductPage.html", data = data, description=description, avgReview=avgReview, review=1)

# Add to wishlist
@app.route("/wishlist", methods=["POST"])
def wishlist():

    # Get the book ID, book data and wishlist
    bookID = request.form.get("wishlist-add")
    tmp = db.execute("SELECT * FROM cart WHERE (userID=:userID AND bookID=:bookID)", userID = session["user_id"], bookID = bookID)
    namePrice = db.execute("SELECT * FROM products WHERE id=:bookID", bookID=bookID)

    # If the isn't in the list, add it in, else leave untouched
    if not tmp:
        db.execute("INSERT INTO cart (userID, bookID, price, bookName) VALUES (:userID, :bookID, :price, :bookName)", userID=session["user_id"], bookID=bookID, price=namePrice[0]["price"], bookName=namePrice[0]["name"])
        return redirect("/cart")
    else:
        # Return the cart
        return redirect("/cart")

# Product purchase page
@app.route("/buy", methods=["POST"])
def buy():
    bookID=0
    # Check if the user is trying to access the purchase page or confirming their purchase.
    if request.form.get("buy"):
        # Retrieve the book data and return page
        bookID = request.form.get("buy")
        bookData = db.execute("SELECT * FROM products WHERE id=:id", id=bookID)
        return render_template("buy.html", data=bookData, text=None)
    elif request.form.get("buyConfirm"):
        # Get the book data and userdata
        bookID = request.form.get("buyConfirm")
        bookData = db.execute("SELECT * FROM products WHERE id=:id", id=bookID)
        userData = db.execute("SELECT * FROM user WHERE id=:id", id=session["user_id"])

        # Verify the user has enough credits
        if float(userData[0]["credits"]) < float(bookData[0]["price"]):
            return render_template("buy.html", data=bookData, text="Insufficient credits.")
        
        # Verify the user has agreed to the terms displayed
        if request.form.get("agree"):
            # Add the book to the user's bookshelf and transaction history
            db.execute("INSERT INTO history (userID, bookID, bookName, paid, date) VALUES (:userID, :bookID, :bookName, :paid, :date)", userID=session["user_id"], bookID=bookID, bookName=bookData[0]["name"], paid=bookData[0]["price"], date=date.today())
            db.execute("INSERT INTO userHistory (userID, bookID, bookName, paid, date) VALUES (:userID, :bookID, :bookName, :paid, :date)", userID=session["user_id"], bookID=bookID, bookName=bookData[0]["name"], paid=bookData[0]["price"], date=date.today())
            
            # Add update the user's credits with new data and remove the book from the wishlist
            credits = float(userData[0]["credits"]) - float(bookData[0]["price"])
            db.execute("UPDATE user SET credits=:credits", credits=credits)
            db.execute("DELETE FROM cart WHERE (userID=:userID AND bookID=:bookID)", userID=session["user_id"], bookID=bookID)
            # Redirect the user to their bookshelf
            return redirect("/bookshelf")        
        else:
            return render_template("buy.html", data=bookData, text="You must agree to the terms to buy!")

@app.route("/download", methods=["POST"])
def download():
    # Return a placeholder file for the download
    return send_file("static/book.pdf")

@app.route("/about", methods=["GET"])
def about():
    # Return the about page
    return render_template("about.html")

@app.route("/search", methods=["POST"])
def search():
    text = request.form.get("search")
    result = []
    # Check for matches on book names
    result = db.execute("SELECT * FROM products WHERE name LIKE ?", '%' + text + '%')
    if not result:
    # Check for matches on author names
        result = db.execute("SELECT * FROM products WHERE author LIKE ?", '%' + text + '%')
    if not result:
    # CHeck for matches on category
        result = db.execute("SELECT * FROM products WHERE category LIKE ?", '%' + text + '%')
    if not result:
    # If no results are found, return a fail variable for the HTML
        return render_template("collections.html", tmp=result, search=1, result=1, fail=1)
    
    # Else just return the results
    return render_template("collections.html", tmp=result, search=1, result=1)

def find(filetype, path):
    result = []
    # Traverse the given filepath and return the contents
    for root, dirs, files in os.walk(path):
        # Iterate over the files list
        for name in files:
            # If the file type at the current iteration matches, append the data
            if fnmatch.fnmatch(name, filetype):
                result.append(os.path.join(name))
    # Return the result to the calling function
    return result[0]

def update():
    # Static path where books are stored
    path = './static/products'

    folders = []
    found = 0

    # Get the current product list
    tmp = db.execute("SELECT * FROM products")

    # Get the book names currently available on the list by recording the names of the folders in that static path
    # and add them to the list
    for root, directories, files in os.walk(path):
        for folder in directories:
            folders.append(os.path.join(root, folder))

    # Check if the book is already in the database, else add it into the database
    for files in folders:
        found = 0
        for rows in tmp:
            # If the book exists, set found to 1, else keep it zero.
            if rows["name"] == (files[18:]):
                found = 1
        if found == 0:
            # Call the find function to find files containing the book details
            price = find('*.price', files)
            author = find('*.author', files)
            category = find('*.category', files)

            # Insert into database
            db.execute("INSERT INTO products (name, price, category, osTime, date, path, author) VALUES (:name, :price, :category, :osTime, :date, :path, :author)", name=files[18:], price=int(price[:-6]), category=category[:-9], osTime=time.time(), date=date.today(), path=files[1:], author=author[:-7])

def updateRating(bookID):
    # Grab all current reviews of the book
    reviews = db.execute("SELECT review FROM reviews WHERE bookID=:bookID", bookID=bookID)
    sum = 0
    totalReviews = 0

    avgReview=0

    # Count the current number of reviews
    for row in reviews:
        sum += int(row["review"])
        totalReviews += 1

    # Calculate an average rating if the sum and totalReviews is not zero (can't divide 0 / 0 !!!!)
    if sum!=0 and totalReviews!=0:
        avgReview = sum/totalReviews

    # Update the database of the new rating
    db.execute("UPDATE products SET rating=:rating WHERE id=:id", rating=round(avgReview), id=bookID)

    # Return the average review
    return round(avgReview)

# Call on the update function the moment the program is started to add any new books to the library.
update()