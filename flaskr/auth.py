from flask import Flask, Blueprint, flash, redirect, render_template, url_for, session, request
from datetime import timedelta
import json

auth_bp = Blueprint("auth", __name__)


@auth_bp.route('/register', methods=["POST", "GET"])
def register():
    auth_bp.permanent_session_lifetime = timedelta(minutes=2)
    session.permanent = True;

    if request.method == "GET":
        return render_template("auth/register.html")

    else:
        error = None
        page_structure = request.form

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
    
        for element in users_data:
            if element["email"] == session["user_data"]["email"]:
                error = "This email is already registered."

            elif element["user_name"] == session["user_data"]["user_name"]:
                error = "This user name is already registered."
        

        if error is not None:
            flash(error)
            return render_template("auth/register.html")

            
        session["user_data"] = {
            "user_name": page_structure["user_name"],
            "email": page_structure["email"],
            "password": page_structure["password"]
        }


        users_data.append(session["user_data"])
        with open("flaskr/db.json", "w") as file:
            file.write(json.dumps(users_data, sort_keys=True, indent=2))


        return redirect(url_for("blog.user"))
        
    
@auth_bp.route('/login', methods=["POST", "GET"])         
def login():
    auth_bp.permanent_session_lifetime = timedelta(minutes=2)
    session.permanent = True;

    if request.method == "GET":
        try:
            session["user_data"]
            return redirect(url_for("blog.user"))
        except:
            return render_template("auth/login.html");
        
    
    else:

        error = None
        page_structure = request.form

        if not page_structure["user_id"]:
            error = "User name or Email is required."

        elif not page_structure["password"]:
            error = "Password is required."

        
        if error is not None:
            flash(error)
            return render_template("auth/login.html")


        input_user_id = page_structure["user_id"]
        input_password = page_structure["password"]

        with open("flaskr/db.json", 'r') as file:
            db = json.load(file);

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
    auth_bp.permanent_session_lifetime = timedelta(minutes=2)
    session.permanent = True;

    if request.method == "GET":
        try:
            session["user_data"]
            return render_template("blog/update.html")
        except:
            return redirect(url_for("blog.index"))
        

    else:
        error = None
        page_structure = request.form

        if (not page_structure["user_name"]) and (not page_structure["email"]) and (not page_structure["password"]):
            error = "Some change is need"
            flash(error)
            return render_template("blog/update.html")
        

        with open("flaskr/db.json") as file:
            users_data = json.load(file)
            

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


        with open("flaskr/db.json", "w") as file:
            file.write(json.dumps(users_data, sort_keys=True, indent=2))

        print(session["user_data"])
        print(users_data)

        return redirect(url_for("blog.user", user_name=session["user_data"]["user_name"]))


@auth_bp.route('/logout', methods=["POST", "GET"])
def logout():

    if request.method == "GET":
        redirect(url_for("blog.index"))


    auth_bp.permanent_session_lifetime = timedelta(minutes=2)
    session.permanent = True;

    session.pop("user_data", None)
    return redirect(url_for("blog.index"))


@auth_bp.route("/delete_account", methods=["GET", "DELETE"])
def delete_account():

    if request.method == "GET":
        redirect(url_for("blog.index"))

    auth_bp.permanent_session_lifetime = timedelta(minutes=2)
    session.permanent = True;

    with open('flaskr/db.json') as file:
        db = json.load(file)
        
    db.remove(session["user_data"])
        
    with open('flaskr/db.json', 'w') as file:
        file.write(json.dumps(db, sort_keys=True, indent=2))

    # And logout the user
    return redirect(url_for("auth.logout"))