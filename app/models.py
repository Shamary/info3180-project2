from . import db


class User(db.Model):
    
    userid=db.Column(db.Integer,primary_key=True)
    fname=db.Column(db.String(50))
    lname=db.Column(db.String(50))
    age=db.Column(db.Integer)
    gender=db.Column(db.String(10));
    uname=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(300))
    
    
    def __init__(self, userid, fname, lname, age, sex, uname, password):
        self.userid = userid
        self.fname = fname
        self.lname = lname
        self.age = age
        self.gender = sex
        self.uname = uname
        self.password = password

    
    def is_authenticated(self):
        return True;
        
    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)    
        
        
class Item(db.Model):
    
    itemid=db.Column(db.Integer,primary_key=True)
    #uname=db.Column(db.String(50),unique=True)
    item_name=db.Column(db.String(50))
    details=db.Column(db.String(255))
    thumbnail=db.Column(db.String(255))
    item_url=db.Column(db.String(255))
    
    
    def __init__(self, itemid, title, details, address, imageUrl):
        self.itemid = itemid
        self.item_name = title
        self.details = details
        self.url = address
        self.thumbnail = imageUrl
    

# Relationship between user and item databases (many to many relationship)
#
wishlist = db.Table('wishlist',
        db.Column('user_id', db.Integer, db.ForeignKey('user.userid')), 
        db.Column('wish_id', db.Integer, db.ForeignKey('wish.itemid')))
        
        
        
        