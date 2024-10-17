from flask import render_template, session, redirect, url_for, flash, request
from app.models import User
from app import db

class AdminController:
    
    def admin(self):

      if request.method != "GET":
        db.session.query(User).delete()
        db.session.commit()
         
      return render_template("admin/admin.html", users = User.query.all())