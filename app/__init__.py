from flask import Flask, session, request
from mvc_flask import FlaskMVC
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "73eeac3fa1a0ce48f381ca1e6d71f077"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
    FlaskMVC(app)

    from app.models import User
    db.init_app(app)
    Migrate(app, db)

    return app