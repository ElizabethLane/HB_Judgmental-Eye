"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    #This returns none if the user is not in the browser session. Now in the 
    #homepage.html we will show the sign up and log in button because satisfy the else. 
    user = session.get("user")

    return render_template("homepage.html",user=user)

@app.route('/users')
def user_list():
    """Show list of users"""
    # Grabbing all of the user objects and storing them into a list called users. This list
    # is being sent to the user_list.html via the rendertemplate. 
    users = User.query.all()
    #QUESTION: can you send lists through rendertemplate? Or does this need to turn to JSON object?
    return render_template("user_list.html", users=users)


@app.route("/register", methods=["GET", "POST"])
def register_process():

    if request.method == "GET":
        return render_template("register_form.html")

    if request.method == "POST":

        #Get the username and password from the form.
        email = request.form.get("email")
        password = request.form.get("password")
        #Add these values to the user table. 


        #Query to see if the username is in the database.
        user = User.query.filter(User.email == email).first()
        

        if user:
            session["user"] = user.user_id
            #add the user_id info to the flask session. user: user_id
            #get the user_id from the user_id => user.user_id  
            
        else:
            #This user is the user we plan to add to the database.
            user = User(email=email,password=password)
            #We are adding the user to the browser session to manage the buttons that
            #are displayed (see / route, it gets the values for the key "user")
            session["user"] = user.email
            #Adding the user as an object to the db session.
            db.session.add(user)
            #Committing the user to the database. 
            db.session.commit()

        return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login_process():

    if request.method == "GET":
        
        return render_template("login.html")


    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter(User.email == email).first()

        #Checking if the user exists in the database.
        if not user:
            flash('Invalid Credentials')
            return render_template("login.html")

        #In the case that the user does exist, does the password they enter match?
        elif user.password == password:
            #telling the browser that a user is logged in.
            session["user"] = user.user_id
            flash('You were successfully logged in.')
            return redirect("/")
        
        #If the password does not match that which is in the database, reload page 
        #and flash invalid credentials. 
        else:
            flash('Invalid Credentials')
            return render_template("login.html")

@app.route('/logout')
def logout_user():
    """Log out the user and delete user from session."""

    flash('You have successfully logged out.')
    del session['user']

    return redirect("/")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
