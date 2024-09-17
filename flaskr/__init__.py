import os
from flask import Flask, Blueprint, session
from datetime import timedelta
from .auth import auth_bp
from .blog import blog_bp

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True);
    app.config.from_mapping(
        SECRET_KEY = 'dev',
    )


    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp)


    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config);


    try:
        os.makedirs(app.instance_path)
    except:
        pass
    

    return app