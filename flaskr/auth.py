from flask import Blueprint, flash, redirect, render_template, url_for, session, request
from datetime import timedelta
import json


# initializing a blueprint
auth_bp = Blueprint("auth", __name__)


@auth_bp.route('/register', methods=["POST", "GET"])
def register():
    """
        Decorator reponsible for register page
    """

    # Setting a session
    auth_bp.permanent_session_lifetime = timedelta(minutes=2)
    session.permanent = True;

    # If access was forced by browser or directed for this root, render the register page
    if request.method == "GET":
        return render_template("auth/register.html")

    else:
        error = None
        # Request the html structure of the page
        page_structure = request.form

        # The keys must match with the HTML components name
        if not page_structure["user_name"]:
            error = "User name is required."

        if not page_structure["email"]:
            error = "Email is required."

        elif not page_structure["password"]:
            error = "Password is required."

        
        if error is not None:
            flash(error)
            return render_template("auth/register.html")
        

        with open("flaskr/db.json") as file:
            users_data = json.load(file)

        # If these data is already registered, inform
        for element in users_data:
            if element["email"] == session["user_data"]["email"]:
                error = "This email is already registered."

            elif element["user_name"] == session["user_data"]["user_name"]:
                error = "This user name is already registered."
        

        if error is not None:
            flash(error)
            return render_template("auth/register.html")


        # Save tha data in the session 
        session["user_data"] = {
            "user_name": page_structure["user_name"],
            "email": page_structure["email"],
            "password": page_structure["password"]
        }


        # Save changes on the Data Base
        users_data.append(session["user_data"])
        with open("flaskr/db.json", "w") as file:
            file.write(json.dumps(users_data, sort_keys=True, indent=2))


        return redirect(url_for("blog.user"))
        
    
@auth_bp.route('/login', methods=["POST", "GET"])         
def login():

    """
        Decorator reponsible for the login page
    """

    # Setting the session
    auth_bp.permanent_session_lifetime = timedelta(minutes=2)
    session.permanent = True;

    # If access was forced by browser or directed for this root
    if request.method == "GET":

        # If the client is already logged, direct to user page
        try:
            session["user_data"]
            return redirect(url_for("blog.user"))
        
        # Else, render the login page
        except:
            return render_template("auth/login.html");
        
    
    else:

        error = None
        # Request the HTML structure of the page
        page_structure = request.form

        # The keys must match with the HTML components
        if not page_structure["user_id"]:
            error = "User name or Email is required."

        elif not page_structure["password"]:
            error = "Password is required."

        
        if error is not None:
            flash(error)
            return render_template("auth/login.html")


        input_user_id = page_structure["user_id"]
        input_password = page_structure["password"]

        # Load the data base
        with open("flaskr/db.json", 'r') as file:
            db = json.load(file);

        # If the datas match, load the user data in the session
        for element in db:
            if( (element["user_name"] == input_user_id or element["email"] == input_user_id) and element["password"] == input_password ):
                session["user_data"] = element
                return redirect(url_for("blog.user", user_name=session["user_data"]["user_name"]))
        
        else:
            error = "User name/email or password incorrect"
            flash(error)
            return render_template("auth/login.html")
        

@auth_bp.route('/update', methods=["POST", "GET"])
def update():

    """
        Decorator responsible for the data update page
    """

    # Setting the session
    auth_bp.permanent_session_lifetime = timedelta(minutes=2)
    session.permanent = True;

    # # If access was forced by browser or directed for this root
    if request.method == "GET":

        # if the client is already logged, render the data update page
        try:
            session["user_data"]
            return render_template("blog/update.html")
    
        # Else, direct to index page
        except:
            return redirect(url_for("blog.index"))
        

    else:
        error = None
        # Request the HTML structure of the page
        page_structure = request.form

        if (not page_structure["user_name"]) and (not page_structure["email"]) and (not page_structure["password"]):
            error = "Some change is need"
            flash(error)
            return render_template("blog/update.html")
        

        # Load the db
        with open("flaskr/db.json") as file:
            users_data = json.load(file)
            

        # Find the current user`s data and replace on the database and session
        # The keys must match with the HTML components
        for element in users_data:
            if element == session["user_data"]:
                if page_structure["user_name"]:
                    session["user_data"]["user_name"] = page_structure["user_name"]
                    element["user_name"] = page_structure["user_name"]

                if page_structure["email"]:
                    session["user_data"]["email"] = page_structure["email"]
                    element["email"] = page_structure["email"]

                if page_structure["password"]:
                    session["user_data"]["password"] = page_structure["password"]
                    element["password"] = page_structure["password"]


        # Save the data base
        with open("flaskr/db.json", "w") as file:
            file.write(json.dumps(users_data, sort_keys=True, indent=2))

        # Direct to user page
        return redirect(url_for("blog.user", user_name=session["user_data"]["user_name"]))


@auth_bp.route('/logout', methods=["POST", "GET"])
def logout():

    """
        Decorator responsible for logout process
    """

    # Setting the session
    session.permanent = True;
    auth_bp.permanent_session_lifetime = timedelta(minutes=2)

    # If access was forced by browser, come back index page
    if request.method == "GET":
        redirect(url_for("blog.index"))


    # pop the user data from the session
    session.pop("user_data", None)

    # return to index page
    return redirect(url_for("blog.index"))


@auth_bp.route("/delete_account", methods=["GET", "DELETE"])
def delete_account():

    """
        Decorator responsible by daccount deletion process
    """


    # If access was forced by browser, come back index page
    if request.method == "GET":
        redirect(url_for("blog.index"))

    # Set the session
    auth_bp.permanent_session_lifetime = timedelta(minutes=2)
    session.permanent = True;

    # Load the db
    with open('flaskr/db.json') as file:
        db = json.load(file)

    # Remove account data from db   
    db.remove(session["user_data"])
    
    # Save
    with open('flaskr/db.json', 'w') as file:
        file.write(json.dumps(db, sort_keys=True, indent=2))

    # Logout the user
    return redirect(url_for("auth.logout"))