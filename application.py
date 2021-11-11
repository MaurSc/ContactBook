import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, err

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///phonebook.db")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            error = "Missing name"
            return render_template("/register.html", error = error)
        password = request.form.get("password")
        if not password:
            error = "Password not match"
            return render_template("/register.html", error = error)
        confirmatio = request.form.get("confirmation")
        if not confirmatio:
            error = "Password not match"
            return render_template("/register.html", error = error)
        if password != confirmatio:
            error = "Password not match"
            return render_template("/register.html", error = error)
        rows = db.execute("SELECT * FROM users WHERE username =?", username)
        if len(rows) != 1:
            passhash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
            insrow = db.execute("INSERT INTO users (username, hash) VALUES (?,?)", username, passhash)
            flash("Registered!")
            return render_template("login.html")
        else:
            error = "Name does exist!"
            return render_template("register.html", error = error)

    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            error = "must provide username"
            return render_template("/login.html", error = error)
        # Ensure password was submitted
        elif not request.form.get("password"):
            error = "must provide password"
            return render_template("/login.html", error = error)
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username=?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            error = "invalid username and/or password"
            return render_template("/login.html", error = error)

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

@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    #I Create a new list for saving all data of DB then I can display it on HTML
    contacts=[]
    #Query for display to the client, his/her name on the header
    user = db.execute("SELECT username FROM users WHERE id =?",session["user_id"])
    name = user[0]["username"]
    rows = db.execute("""
                        SELECT nameContact,number,email
                        FROM contact
                        WHERE user_id=?
                        ORDER BY nameContact
                        """,session["user_id"])
    for row in rows:
        contacts.append({
            "name":row["nameContact"],
            "number":row["number"],
            "email":row["email"]
        })
    return render_template("/index.html",user=name, contacts=contacts)
@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Get form to add new contact."""
    if request.method == "POST":
        name=request.form.get("name")
        if not name:
            error = "Must provide Name"
            return render_template("add.html", error = error)
        phone=request.form.get("phone")
        if not phone:
            error = "Must provide Phone"
            return render_template("add.html", error = error)
        email=request.form.get("email")
        if not email:
            error = "Must provide Email"
            return render_template("add.html", error = error)
        #I do not want there to be several contacts with the same name on my agenda, for this reason, I avoid repeating names
        namme = db.execute("SELECT nameContact FROM contact WHERE nameContact=? AND user_id=?",name,session["user_id"])
        if len(namme) >= 1:
            error = "Name of contact does exist on your phonebook!"
            return render_template("add.html", error = error)
        rows = db.execute("SELECT * FROM contact WHERE nameContact=? AND number=? AND email=? AND user_id=?",name,phone,email,session["user_id"])
        #include a query for knew, if contact is same to another for not add to this
        if len(rows) >= 1:
            error = "Contact does exist on your phonebook!"
            return render_template("add.html", error = error)
        row = db.execute("INSERT INTO contact (nameContact,number,email,user_id) VALUES (?,?,?,?)",name,phone,email,session["user_id"])
        flash("¡Contact Added!")
        return redirect("/")
    return render_template("add.html")


@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    """Edit contacts"""
    contacts=[]
    contac=[]
    nameC="none"
    rows = db.execute("""
                        SELECT nameContact,number,email,id
                        FROM contact
                        WHERE user_id=?
                        ORDER BY nameContact
                        """,session["user_id"])
    for row in rows:
        contacts.append({
            "id":row["id"],
            "name":row["nameContact"],
            "number":row["number"],
            "email":row["email"]
        })
    if request.method == "POST":
        nameC = request.form.get("name")
        for row in rows:
            if row["nameContact"] == nameC:
                contac.append({
                    "id":row["id"],
                    "name":row["nameContact"],
                    "number":row["number"],
                    "email":row["email"]
                })
                return render_template("change.html",contac=contac)
        newNumber = request.form.get("number")
        newMail = request.form.get("email")
        elid = request.form.get("elid")
        if newNumber and newMail:
            row = db.execute("""
                                UPDATE contact
                                SET number=?, email=?
                                WHERE id=?
                                """,newNumber,newMail,elid)
            flash("Change succesfull")
            return render_template("edit.html",contacts=contacts)
        if newNumber:
            row = db.execute("""
                                UPDATE contact
                                SET number=?
                                WHERE id=?
                                """,newNumber,elid)
            flash("Change succesfull")
            return render_template("edit.html",contacts=contacts)
        elif newMail:
            row = db.execute("""
                                UPDATE contact
                                SET email=?
                                WHERE id=?
                                """,newMail,elid)
            flash("Change succesfull")
            return render_template("edit.html",contacts=contacts)
        else:
            error="Some data doesn't went provide"
            return render_template("edit.html",error=error, contacts=contacts)
        return render_template("edit.html", contacts=contacts)
    return render_template("edit.html", contacts=contacts)

@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    """Delete contacts"""
    contacts=[]
    rows = db.execute("""
                        SELECT nameContact,number,email,id
                        FROM contact
                        WHERE user_id=?
                        ORDER BY nameContact
                        """,session["user_id"])
    for row in rows:
        contacts.append({
            "id":row["id"],
            "name":row["nameContact"],
            "number":row["number"],
            "email":row["email"]
        })

    if request.method == "POST":
        nameC = request.form.get("name")
        delete = db.execute("""
                                DELETE
                                FROM contact
                                WHERE nameContact=?
                                AND user_id=?
                                """,nameC,session["user_id"])
        return redirect("/")
    return render_template("delete.html",contacts=contacts)



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return err(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
