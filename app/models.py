from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    
    def __repr__(self):
        return '<User {}>'.format(self.username)   

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Textfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    extension = db.Column(db.String(5))
    body = db.Column(db.String(2500))
    timestamp = db.Column(db.DateTime, index=True, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    
    def __repr__(self):
        return '<Text {}>'.format(self.body)