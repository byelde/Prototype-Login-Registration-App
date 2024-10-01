from flask import render_template, request, redirect, url_for, session, flash
from app.models import User
from app import db

class BlogController:
    
    def update(self):

      if request.method != "PUT":

          try:

            user = User.query.filter_by(email=session["user"]["email"]).first()
            return render_template("blog/update.html")
      
          except:

            return redirect(url_for("home.index"))
          

      else:
          
          error = None

          curr_pwd = request.form.get("curr_pwd")
          new_pwd  = request.form.get("new_pwd")

          if not (curr_pwd and new_pwd) :
            error = "Data is required."
            flash(error)
            return render_template("blog/update.html")
          
          user = User.query.filter_by(email=session["user"]["email"]).first()

          if not (user.verify_password(curr_pwd) ):
            error = "Wrong Password."
            flash(error)
            return render_template("blog/update.html")
          
          user.setPassword(new_pwd)
          db.session.commit()
                    
          return redirect(url_for("blog.user", user_name=session["user"]["user_name"]))

    
    def user(self):
      return render_template("blog/user.html", user_name=session["user"]["user_name"])