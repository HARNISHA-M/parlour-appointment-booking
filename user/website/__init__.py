from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
from distutils.log import debug
from email import message
from sre_constants import SUCCESS
from flask_mail import Mail,Message

db = SQLAlchemy()
mail=Mail()
DB_NAME = "parlour.db"
def create_app():
    app = Flask(__name__)
    app.secret_key="Secret key"
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:9080Nisha!@localhost/parlour"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    app.config['MAIL_SERVER'] ='smtp.gmail.com'
    app.config['MAIL_PORT'] =465
    app.config['MAIL_USERNAME']='harinisham.20cse@kongu.edu'
    app.config['MAIL_PASSWORD']="9080@nisha"
    app.config['MAIL_USE_TLS'] =False
    app.config['MAIL_USE_SSL']=True
    db.init_app(app)
    mail.init_app(app)
    
    from .views import views
    app.register_blueprint(views, url_prefix='/')
    create_database(app)
    login_manager=LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)
    from .models import User
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

def create_database(app): 
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        
