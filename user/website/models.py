from . import db
from flask_login import UserMixin

class bookingdb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100))
    email = db.Column(db.String(100))
    address = db.Column(db.String(100))
    phne=db.Column(db.String(30))
    package=db.Column(db.String(50))
    date=db.Column(db.String(50))
    username=db.Column(db.String(100))
    status=db.Column(db.String(100))
    def __init__(self,name,email,address,phne,package,date,username,status):
        self.name = name
        self.email = email
        self.address = address
        self.phne = phne
        self.package = package
        self.date = date
        self.username=username
        self.status=status
       
class galleryImageUpload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(500))
    final_img = db.Column(db.Text(4294000000), nullable=False)

    def __init__(self,name,final_img):
        self.filename=name
        self.final_img=final_img

class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    usertype = db.Column(db.String(20), nullable=False)