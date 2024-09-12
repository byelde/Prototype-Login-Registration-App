from flask import Flask, flash, redirect, render_template, url_for, session, request
from datetime import timedelta
import json


app = Flask(__name__)
app.secret_key = "FOGO"
app.permanent_session_lifetime = timedelta(minutes=2)


# Define the initial root
@app.route("/", methods=["GET", "POST"])
def init():
    # Set a non-volatile session
    session.permanent = True;
    return render_template("main.html")
        

# Define the register page
@app.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "GET":
        # If the client is redirected for this route, load the page
        return render_template("register.html")
    
    else:  
        page_structure = request.form

        session["user_data"] = {
            "user": page_structure["user"],
            "email": page_structure["email"],
            "password": page_structure["password"]
        }

        with open('data/test.json') as file:
            listObj = json.load(file)
        
        if session["user_data"] not in listObj:
            listObj.append(session["user_data"])
        else:
            flash("")
        
        with open('data/test.json', 'w') as file:
            file.write(json.dumps(listObj, sort_keys=True, indent=2))

        return redirect(url_for("user_page"))


@app.route("/login", methods=["GET", "POST"])
def login_page():

    if request.method == "POST":
        page_structure = request.form

        input_email = page_structure["email"]
        input_password = page_structure["password"]

        with open("data/test.json", 'r') as file:
            all_data = json.load(file);

        for element in all_data:
            if( element["email"] == input_email and element["password"] == input_password ):
                session["user_data"] = element
                return redirect(url_for("user_page"))
        else:
            flash("Incorrect Login.")
            return render_template("login.html")


    else:
        return render_template("login.html")


@app.route("/user", methods=["GET", "POST"])
def user_page():
    if "user_data" in session:
        return render_template("user.html", user_name=session["user_data"]["user"])
    else:
        return redirect(url_for("init"))
    

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("user_data", None)
    return redirect(url_for("init"))


@app.route("/delete_account", methods=["GET", "POST"])
def delete_account():
    with open('data/test.json') as file:
        listObj = json.load(file)
        
    listObj.remove(session["user_data"])
        
    with open('data/test.json', 'w') as file:
        file.write(json.dumps(listObj, sort_keys=True, indent=2))

    return redirect(url_for("logout"))


if __name__ == "__main__":
    app.run(debug=True, port=8001)