import os
from flask import Flask, Blueprint, session
from datetime import timedelta
from .auth import auth_bp
from .blog import blog_bp

def create_app(test_config=None):

    """
        Init project method 
    """

    # initializing the a Flask App 
    app = Flask(__name__, instance_relative_config=True);
    app.config.from_mapping( SECRET_KEY = 'dev' )

    # Importing Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp)


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config);


    try:
        # forcing the existence of the directory "instance" 
        os.makedirs(app.instance_path)
    except:
        pass
    

    return app