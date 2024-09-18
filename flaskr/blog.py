from flask import Blueprint, render_template, session

# initializing a blueprint
blog_bp = Blueprint("blog", __name__)

@blog_bp.route("/", methods=["GET", "POST"])
def index():

    """
        Decorator responsible by indexpage
    """

    return render_template("blog/index.html")


@blog_bp.route("/user", methods=["GET", "POST"])
def user():

    """
        Decorator responsible by the user page
    """

    return render_template("blog/user.html", user_name=session["user_data"]["user_name"])