from flask import Flask, Blueprint, flash, redirect, render_template, url_for, session, request
import json

blog_bp = Blueprint("blog", __name__)

@blog_bp.route("/", methods=["GET", "POST"])
def index():
    return render_template("blog/index.html")


@blog_bp.route("/user", methods=["GET", "POST"])
def user():
    return render_template("blog/user.html", user_name=session["user_data"]["user_name"])