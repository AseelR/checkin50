import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from datetime import datetime, date

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///checkin50.db")

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Referenced Finance Problem Set to determine objects for importation and to craft base of register page

# Other references used:
# https://www.geeksforgeeks.org/iterate-over-characters-of-a-string-in-python/
# https://www.w3schools.com/python/ref_string_isnumeric.asp#:~:text=The%20isnumeric()%20method%20returns,%2C%20and%20the%20%2D%20and%20the%20.
# https://www.tutorialspoint.com/How-to-check-if-a-character-is-upper-case-in-Python#:~:text=The%20Python%20standard%20library%20has,is%20lowercase%2C%20it%20returns%20FALSE.
# https://www.w3schools.com/python/python_operators.asp
# https://www.tutorialspoint.com/increment-and-decrement-operators-in-python
# https://realpython.com/null-in-python/#understanding-null-in-python
# https://www.w3schools.com/sql/sql_count_avg_sum.asp
# https://www.geeksforgeeks.org/find-length-of-a-string-in-python-4-ways/
# https://www.w3schools.com/tags/att_button_value.asp
# https://www.w3schools.com/sql/trysql.asp?filename=trysql_delete
# https://www.geeksforgeeks.org/python-dictionary/
# https://www.digitalocean.com/community/tutorials/how-to-use-web-forms-in-a-flask-application#step-3-handling-form-requests-%20https:/www.digitalocean.com/community/tutorials/how-to-use-web-forms-in-a-flask-application#step-3-handling-form-requests
# https://flask.palletsprojects.com/en/2.0.x/patterns/flashing/
# https://www.w3schools.com/sql/sql_update.asp
# https://www.digitalocean.com/community/tutorials/python-string-equals
# https://stackoverflow.com/questions/43811779/use-many-submit-buttons-in-the-same-form
# https://www.geeksforgeeks.org/extract-time-from-datetime-in-python/
# https://stackoverflow.com/questions/53162/how-can-i-do-a-line-break-line-continuation-in-python
# https://www.w3schools.com/tags/att_select_form.asp
# https://www.programiz.com/python-programming/datetime
# https://blog.finxter.com/dict-to-list/
# https://www.geeksforgeeks.org/python-find-dictionary-matching-value-in-list/
# https://www.studytonight.com/python-howtos/how-to-get-a-list-of-values-from-a-list-of-dictionary
# https://statisticsglobe.com/check-value-exists-list-dictionaries-python
# Aseel received advice from Omar Abdel-Haq on implementing formpage

# Helper functions

def login_required(f):
    # References https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/, using similar code from the finance problem set
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# Main functions

@app.route("/")
def layout():
    # if no user is logged in, render logged out homepage
    if session.get("user_id") is None:
        # activities = db.execute("SELECT * from activities")
        return render_template("logouthomepage.html")
    # if some user is logged in, render logged in homepage
    else:
        #select only meals from today
        user_meals = db.execute("SELECT * FROM meals JOIN Accounts ON Accounts.user_id = meals.user_id WHERE date(timestamp) >= DATE('now') AND date(timestamp) < DATE('now', '+1 day') AND Accounts.user_id = ?", session["user_id"])
        user_study = db.execute("SELECT * FROM study JOIN Accounts ON Accounts.user_id = study.user_id WHERE date(timestamp) >= DATE('now') AND date(timestamp) < DATE('now', '+1 day') AND Accounts.user_id = ?", session["user_id"])
        user_exercise = db.execute("SELECT * FROM exercise JOIN Accounts ON Accounts.user_id = exercise.user_id WHERE date(timestamp) >= DATE('now') AND date(timestamp) < DATE('now', '+1 day') AND Accounts.user_id = ?", session["user_id"])
        user_chill = db.execute("SELECT * FROM chill JOIN Accounts ON Accounts.user_id = chill.user_id WHERE date(timestamp) >= DATE('now') AND date(timestamp) < DATE('now', '+1 day') AND Accounts.user_id = ?", session["user_id"])
        user_username = db.execute("SELECT username from Accounts WHERE user_id = ?", session["user_id"])

        return render_template("loginhomepage.html", meals = user_meals, study = user_study, exercise = user_exercise, chill = user_chill, username = user_username[0]["username"])



# Pre-Login

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Username pre-steps
        username = request.form.get("user")
        if not username:
            registererror = 'Must create username'
            return render_template("register.html",registererror = registererror)
        usernameslist = db.execute("SELECT user_id FROM Accounts WHERE username = ?", username)

        # Password pre-steps
        passlength = len(request.form.get("password"))
        if not passlength:
            registererror = 'Must set password'
            return render_template("register.html",registererror = registererror)
        number = 0
        capital = 0
        symbol = 0
        symbolarray = ["~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-"]

        # Count number of numbers, capitals, and symbol in password
        for element in request.form.get("password"):
            if element.isnumeric():
                number += 1
            if element.isupper():
                capital += 1
            if element in symbolarray:
                symbol += 1

        # Result in registration error if username already taken, password insecure, or password/confirmation don't match
        while len(usernameslist) > 0 or number < 1 or capital < 1 or passlength <= 8 or request.form.get("password") != request.form.get("passconfirm"):
            if len(usernameslist) > 0:
                registererror =  'Username already taken'
            elif request.form.get("password") != request.form.get("passconfirm"):
                registererror = 'Passwords do not match'
            else:
                registererror = 'Password insecure'
            return render_template("register.html",registererror = registererror)

        # generate passhash only if all requirements are met
        passhash = generate_password_hash(request.form.get("password"))

        db.execute("INSERT INTO Accounts(username, password) VALUES(?,?)", username, passhash)
        user = db.execute("SELECT user_id FROM Accounts WHERE username = ?", username)
        session["user_id"] = user[0]["user_id"]
        return redirect("/")

    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Query database for username - from finance problem set
        rows = db.execute("SELECT * FROM Accounts WHERE username = ?", request.form.get("username"))

        # Check if username exists and password is correct and if not, reload empty page
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            loginerror = 'Username or Password are incorrect'
            return render_template("login.html", loginerror = loginerror)

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]
        return redirect("/")

    else:
        return render_template("login.html")

# Post-Login

# Sidebar - Main
@app.route("/formpage", methods=["GET", "POST"])
@login_required
def formpage():
    if request.method == "GET":
        return render_template("formpage.html")
    else:

        # Set today's date and categories for each activity
        today = str(date.today())
        mealtype = ["Breakfast", "Lunch", "Dinner"]
        studytype = ["Study Session 1", "Study Session 2", "Study Session 3"]
        chilltype = ["Chill Session 1", "Chill Session 2", "Chill Session 3"]

        # iterate through all three input slots for meals
        for i in [0, 1, 2]:
            if (request.form.get(f"mealstart{i}") != "") and (request.form.get(f"mealend{i}") != ""):

                # format start and end times
                mealstart = datetime.strptime(today + request.form.get(f"mealstart{i}"), '%Y-%m-%d%H:%M')
                mealend = datetime.strptime(today + request.form.get(f"mealend{i}"), '%Y-%m-%d%H:%M')
                mealstart.time
                mealend.time

                # query for all meals from that day from the same mealtype
                meal_type = db.execute("SELECT * FROM meals WHERE mealtype = ? AND user_id = ? AND date(timestamp) >= DATE('now') AND date(timestamp) < DATE('now', '+1 day')", mealtype[i], session["user_id"])

                # if a meal already exists with these specifics, update. if not, add
                if len(meal_type) > 0:
                    db.execute("UPDATE meals SET dhall = ?, mealstart = ?, mealend = ? WHERE user_id = ? AND mealtype = ? AND date(timestamp) >= DATE('now') AND date(timestamp) < DATE('now', '+1 day')", \
                            request.form.get(f"dhall{i}"), mealstart.strftime("%I:%M %p"), mealend.strftime("%I:%M %p"), session["user_id"], mealtype[i])
                else:
                    db.execute("INSERT INTO meals (user_id, mealtype, dhall, mealstart, mealend) VALUES (?, ?, ?, ?, ?)", \
                            session["user_id"], mealtype[i], request.form.get(f"dhall{i}"), mealstart.strftime("%I:%M %p"), mealend.strftime("%I:%M %p"))

        # iterate through all three input slots for studying
        for i in [0, 1, 2]:
            if (request.form.get(f"studystart{i}") != "") and (request.form.get(f"studyend{i}") != ""):

                # format start and end times
                studystart = datetime.strptime(today + request.form.get(f"studystart{i}"), '%Y-%m-%d%H:%M')
                studyend = datetime.strptime(today + request.form.get(f"studyend{i}"), '%Y-%m-%d%H:%M')
                studystart.time
                studyend.time

                # query for all study sessions from that day from the same study session number
                study_type = db.execute("SELECT * FROM study WHERE studytype = ? AND user_id = ? AND date(timestamp) >= DATE('now') AND date(timestamp) < DATE('now', '+1 day')", studytype[i], session["user_id"])

                # if a study session already exists with these specifics, update. if not, add
                if len(study_type) > 0:
                     db.execute("UPDATE study SET study = ?, studystart = ?, studyend = ? WHERE user_id = ? AND studytype = ? AND date(timestamp) >= DATE('now') AND date(timestamp) < DATE('now', '+1 day')", \
                            request.form.get(f"study{i}"), studystart.strftime("%I:%M %p"), studyend.strftime("%I:%M %p"), session["user_id"], studytype[i])
                else:
                    db.execute("INSERT INTO study (user_id, studytype, study, studystart, studyend) VALUES (?, ?, ?, ?, ?)", \
                            session["user_id"], studytype[i], request.form.get(f"study{i}"), studystart.strftime("%I:%M %p"), studyend.strftime("%I:%M %p"))

        # iterate through all three input slots for chill
        for i in [0, 1, 2]:
            if (request.form.get(f"chillstart{i}") != "") and (request.form.get(f"chillend{i}") != ""):

                # format start and end times
                chillstart = datetime.strptime(today + request.form.get(f"chillstart{i}"), '%Y-%m-%d%H:%M')
                chillend = datetime.strptime(today + request.form.get(f"chillend{i}"), '%Y-%m-%d%H:%M')
                chillstart.time
                chillend.time

                # query for all chill sessions from that day from the same chill session number
                chill_type = db.execute("SELECT * FROM chill WHERE chilltype = ? AND user_id = ? AND date(timestamp) >= DATE('now') AND date(timestamp) < DATE('now', '+1 day')", chilltype[i], session["user_id"])

                # if a chill time already exists with these specifics, update. if not, add
                if len(chill_type) > 0:
                    db.execute("UPDATE chill SET chill = ?, chillstart = ?, chillend = ? WHERE user_id = ? AND chilltype = ? AND date(timestamp) >= DATE('now') AND date(timestamp) < DATE('now', '+1 day')", \
                            request.form.get(f"chill{i}"), chillstart.strftime("%I:%M %p"), chillend.strftime("%I:%M %p"), session["user_id"], chilltype[i])
                else:
                    db.execute("INSERT INTO chill (user_id, chilltype, chill, chillstart, chillend) VALUES (?, ?, ?, ?, ?)", \
                        session["user_id"], chilltype[i], request.form.get(f"chill{i}"), chillstart.strftime("%I:%M %p"), chillend.strftime("%I:%M %p"))

        # for input field for exercise
        if (request.form.get("exercisestart") != "") and (request.form.get("exerciseend") != ""):

                # format start and end times
                exercisestart = datetime.strptime(today + request.form.get("exercisestart"), '%Y-%m-%d%H:%M')
                exerciseend = datetime.strptime(today + request.form.get("exerciseend"), '%Y-%m-%d%H:%M')
                exercisestart.time
                exerciseend.time

                # query for all exercise session from that day
                exercise_today = db.execute("SELECT * FROM exercise WHERE user_id = ? AND date(timestamp) >= DATE('now') AND date(timestamp) < DATE('now', '+1 day')", session["user_id"])

                # if an exercise time already exists with these specifics, update. if not, add
                if len(exercise_today) > 0:
                    db.execute("UPDATE exercise SET exercise = ?, exercisestart = ?, exerciseend = ? WHERE user_id = ? AND date(timestamp) >= DATE('now') AND date(timestamp) < DATE('now', '+1 day')", \
                            request.form.get(f"exercise"), exercisestart.strftime("%I:%M %p"), exerciseend.strftime("%I:%M %p"), session["user_id"])
                else:
                    db.execute("INSERT INTO exercise (user_id, exercise, exercisestart, exerciseend) VALUES (?, ?, ?, ?)", \
                            session["user_id"], request.form.get("exercise"), exercisestart.strftime("%I:%M %p"), exerciseend.strftime("%I:%M %p"))

        return redirect("/")


@app.route("/meal", methods=["GET"])
@login_required
def meal():
     #select only meals from today
     all_meals = db.execute("SELECT * FROM meals JOIN Accounts ON Accounts.user_id = meals.user_id WHERE date(timestamp) >= DATE('now') AND date(timestamp) < DATE('now', '+1 day') AND (username in (SELECT friend2username FROM friends WHERE friend1username = (SELECT username FROM Accounts WHERE user_id = ? AND friend2accept = ?)))", session["user_id"], "yes")
     return render_template("meal.html", meals = all_meals)


@app.route("/study")
@login_required
def study():
     #select only study locations from today
    all_study = db.execute("SELECT * FROM study JOIN Accounts ON Accounts.user_id = study.user_id WHERE date(timestamp) >= DATE('now') AND date(timestamp) < DATE('now', '+1 day') AND (username in (SELECT friend2username FROM friends WHERE friend1username = (SELECT username FROM Accounts WHERE user_id = ? AND friend2accept = ?)))", session["user_id"], "yes")
    return render_template("study.html", study = all_study)

@app.route("/exercise")
@login_required
def exercise():
    #select only exercise from today
    all_exercise = db.execute("SELECT * FROM exercise JOIN Accounts ON Accounts.user_id = exercise.user_id WHERE date(timestamp) >= DATE('now') AND date(timestamp) < DATE('now', '+1 day') AND (username in (SELECT friend2username FROM friends WHERE friend1username = (SELECT username FROM Accounts WHERE user_id = ? AND friend2accept = ?)))", session["user_id"], "yes")
    return render_template("exercise.html", exercise = all_exercise)

@app.route("/chill")
@login_required
def chill():
    #select only chill from today
    all_chill = db.execute("SELECT * FROM chill JOIN Accounts ON Accounts.user_id = chill.user_id WHERE date(timestamp) >= DATE('now') AND date(timestamp) < DATE('now', '+1 day') AND (username in (SELECT friend2username FROM friends WHERE friend1username = (SELECT username FROM Accounts WHERE user_id = ? AND friend2accept = ?)))", session["user_id"], "yes")
    return render_template("chill.html", chill = all_chill)

# Sidebar - Dropdown box

@app.route("/addfriend", methods=["GET", "POST"])
@login_required
def addfriend():
    if request.method == "POST":
        friend = request.form.get("friendname")
        if not friend:
            return redirect("/addfriend")
        user = db.execute("SELECT username FROM Accounts WHERE user_id = ?", session["user_id"])

         # List of dictionaries of all of the people the user has requested to be friends with and that they've accepted the request
        yourfriends = db.execute("SELECT friend2username FROM friends WHERE friend1username = (SELECT username FROM accounts WHERE user_id = ?) AND friend2accept = ?", session["user_id"], "yes")

        # List of total number of entries in the above dictionary (for total friend count)
        friendstotal = db.execute("SELECT COUNT(friend2username) FROM friends WHERE friend1username = (SELECT username FROM accounts WHERE user_id = ?) AND friend2accept = ?", session["user_id"], "yes")
        friendsnum = friendstotal[0]["COUNT(friend2username)"]

        # List of dictionaries of all of the people that have requested to be friends with the user, whom they have not replied to the friend request of
        friendspending = db.execute("SELECT friend1username FROM friends WHERE friend2username = (SELECT username FROM accounts where user_id = ?) AND friend2accept = ?", session["user_id"], "pending")

        # check if user is sending request to themself
        if friend == user[0]["username"]:
            error = 'You cannot be friends with yourself!'
            return render_template("addfriend.html", error = error, friendtotal = friendsnum, friendspending = friendspending, yourfriends = yourfriends)

        # List of users with accounts
        accounts = db.execute("SELECT username FROM Accounts")

        # check if user is sending request to user who doesn't exist
        if not any(friend in d.values() for d in accounts):
            error = 'This user does not exist'
            return render_template("addfriend.html", error = error, friendtotal = friendsnum, friendspending = friendspending, yourfriends = yourfriends)

        # check if friendship/request already exists
        friendship = db.execute("SELECT id FROM friends WHERE friend1username = ? AND friend2username = ?", user[0]["username"], friend)
        if len(friendship) > 0:
            error = 'This user is already your friend or request still pending'
            return render_template("addfriend.html", error = error, friendtotal = friendsnum, friendspending = friendspending, yourfriends = yourfriends)

        # create friendship pairing
        db.execute("INSERT INTO friends(friend1username, friend2username, friend2accept) VALUES(?,?,?)", user[0]["username"], friend, "pending")
        return redirect("/addfriend")

    else:
        # List of dictionaries of all of the people the user has requested to be friends with and that they've accepted the request
        yourfriends = db.execute("SELECT friend2username FROM friends WHERE friend1username = (SELECT username FROM accounts WHERE user_id = ?) AND friend2accept = ?", session["user_id"], "yes")

        # List of total number of entries in the above dictionary (for total friend count)
        friendstotal = db.execute("SELECT COUNT(friend2username) FROM friends WHERE friend1username = (SELECT username FROM accounts WHERE user_id = ?) AND friend2accept = ?", session["user_id"], "yes")
        friendsnum = friendstotal[0]["COUNT(friend2username)"]

        # List of dictionaries of all of the people that have requested to be friends with the user, whom they have not replied to the friend request of
        friendspending = db.execute("SELECT friend1username FROM friends WHERE friend2username = (SELECT username FROM accounts where user_id = ?) AND friend2accept = ?", session["user_id"], "pending")

        return render_template("addfriend.html", friendtotal = friendsnum, friendspending = friendspending, yourfriends = yourfriends)

@app.route("/removefriend", methods=["POST"])
def removefriend():
     # remove from own friend list
    if request.method == "POST":
        # get name of friend from select menu of your own friends
        friend = request.form.get("removefriend")
        if not friend:
            return redirect("/addfriend")

        # delete the entry of that friendship
        db.execute("DELETE FROM friends WHERE friend1username = (SELECT username FROM accounts WHERE user_id = ?) AND friend2username = ?", session["user_id"], friend)
        return redirect("/addfriend")

@app.route("/acceptrequest", methods=["POST"])
def acceptrequest():
     # get name of user making request
    if request.method == "POST":
        friend = request.form.get("request")
        if not friend:
            return redirect("/addfriend")
        if request.form['button'] == 'Accept':
            # Change their pending request to accepted
            db.execute("UPDATE friends SET friend2accept = ? WHERE friend1username = ? AND friend2username = (SELECT username FROM accounts WHERE user_id = ?)", "yes", friend, session["user_id"])
        elif request.form['button'] == 'Remove':
            # Delete their friendship from the list
             db.execute("DELETE FROM friends WHERE friend2username = (SELECT username FROM accounts WHERE user_id = ?) AND friend1username = ? AND friend2accept = ?", session["user_id"], friend, "pending")
        return redirect("/addfriend")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
