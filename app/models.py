from . import db


class User(db.Model):
    
    id=db.Column(db.Integer,primary_key=True)
    fname=db.Column(db.String(50))
    lname=db.Column(db.String(50))
    age=db.Column(db.Integer)
    gender=db.Column(db.String(10));
    uname=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(300))
    
    def is_authenticated(self):
        return True;