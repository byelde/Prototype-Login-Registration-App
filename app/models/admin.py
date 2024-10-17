from app.models import User 
from werkzeug.security import generate_password_hash, check_password_hash

class Admin(User):
    pass