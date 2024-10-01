from flask import render_template, session, redirect, url_for, flash, request
from app.models import User
from app import db

class AuthController:
    

    def login(self):

      if request.method == "GET":

        try:
          if(session["user"]):
            return redirect(url_for("blog.user", user_name = session["user"]["user_name"]))

        except:
          return render_template("auth/login.html");
          
      else:
          
        error = None

        email     = request.form.get("email")
        password  = request.form.get("password")

        if not (email and password ) :
          error = "Data is required."
          flash(error)
          return render_template("auth/login.html")
        
        user = User.query.filter_by(email=email).first()

        if not user:
          error = "User not registered."
          flash(error)
          return render_template("auth/login.html")
        
        if not user.verify_password(password):
          error = "Wrong Password."
          flash(error)
          return render_template("auth/login.html")

        session["user"] = {"user_name":user.getUserName(), 
                           "email":user.getEmail()}

        return redirect(url_for("blog.user", user_name = session["user"]["user_name"]))
        

    def register(self):
      if request.method == "GET":

        try:
          if(session["user"]):
            return redirect(url_for("blog.user", user_name = session["user"]["user_name"]))

        except:
          return render_template("auth/register.html");
          
      else:
          
        error = None

        user_name = request.form.get("user_name")
        email     = request.form.get("email")
        password  = request.form.get("password")

        if not (user_name and email and password ) :
                error = "Data is required."
                flash(error)
                return render_template("auth/register.html")
        
        user = User(user_name, email, password)

        session["user"] = {"user_name":user.getUserName(), 
                           "email":user.getEmail()}

        try:
          db.session.add(user)
          db.session.commit()

        except:
          error = "Username o Email already taken."
          flash(error)
          return render_template("auth/register.html")

        return redirect(url_for("blog.user", user_name = user.getUserName()))


    def delete(self):

      if request.method != "DELETE" or not session["user"]:
          return redirect(url_for("home.index"))

      else:

        user = User.query.filter_by(email=session['user']['email']).first()
        db.session.delete(user)
        db.session.commit()

        return redirect(url_for("auth.logout"))


    def logout(self):
      if request.method == "GET":
          redirect(url_for("home.index"))

      session.pop("user", None)

      return redirect(url_for("home.index"))