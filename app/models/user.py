from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id        = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String, nullable=False, unique=True)
    email     = db.Column(db.String, nullable=False, unique=True)
    password  = db.Column(db.String, nullable=False)


    def __init__(self, user_name, email, password):
        self.user_name = user_name
        self.email     = email
        self.password  = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)
    
    def setPassword(self, new_pwd):
        self.password  = generate_password_hash(new_pwd)
    
    def getUserName(self):
        return self.user_name
    
    def getEmail(self):
        return self.email