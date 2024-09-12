from flask import Flask, flash, redirect, render_template, url_for, session, request
from datetime import timedelta
import json

# Starting a Flask app
app = Flask(__name__)

# Define the secret_key (needed to use HTTP methods)
app.secret_key = "FOGO"

# Define the session lifetime
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
    # If the arrival methods is GET, load the page
    if request.method == "GET":
        return render_template("register.html")
    
    else:
        # If the arrival methods is POST, register the user with the data obtained
        page_structure = request.form

        session["user_data"] = {
            "user": page_structure["user"],
            "email": page_structure["email"],
            "password": page_structure["password"]
        }

        with open('data/test.json') as file:
            listObj = json.load(file)
        

        # If the user is already registered reload the page with a flash
        for element in listObj:
            if element["email"] == session["user_data"]["email"]:
                flash("This email is already registered")
                return render_template("register.html")
            
        # Else, register the user
        listObj.append(session["user_data"])
        
        # Save the user register in the data base
        with open('data/test.json', 'w') as file:
            file.write(json.dumps(listObj, sort_keys=True, indent=2))

        return redirect(url_for("user_page"))



#Define the login page
@app.route("/login", methods=["GET", "POST"])
def login_page():

    # Checkin if the login data obtained is registered in the data base 
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
            
        # Else reload the page with flash
        else:
            flash("Incorrect Login.")
            return render_template("login.html")


    else:
        return render_template("login.html")



# Define user`s page
@app.route("/user", methods=["GET", "POST"])
def user_page():
    # If there is a user logged, load the page satisfying the variable {{user_name}} setted in "user.html"
    if "user_data" in session:
        return render_template("user.html", user_name=session["user_data"]["user"])
    
    # Else redirect to the main page
    else:
        return redirect(url_for("init"))
    


# Define a logout process
@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("user_data", None)
    return redirect(url_for("init"))



# Define a database delete account process
@app.route("/delete_account", methods=["GET", "POST"])
def delete_account():
    with open('data/test.json') as file:
        listObj = json.load(file)
        
    listObj.remove(session["user_data"])
        
    with open('data/test.json', 'w') as file:
        file.write(json.dumps(listObj, sort_keys=True, indent=2))

    # And logout the user
    return redirect(url_for("logout"))



if __name__ == "__main__":
    app.run(debug=True, port=8001)