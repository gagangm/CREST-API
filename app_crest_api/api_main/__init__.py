# Import flask and template operators
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import datetime
# from flask.ext.permissions.models import UserMixin
# Define the WSGI application object
#app = Flask(__name__,template_folder='templates')
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

db.init_app(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer , primary_key=True)
    username = db.Column('username', db.String(20), unique=True , index=True)
    password = db.Column('password' , db.String(10))
    email = db.Column('email',db.String(50),unique=True , index=True)
    site_url = db.Column('Site',db.String(50),unique=True)
    api_server = db.Column('api_server' ,db.String(100),default='')
#     role = db.Column('Role', db.String(10))
    registered_on = db.Column('registered_on' , db.DateTime)
    
    def __init__(self , username ,password , email, site_url, api_server, role):
        self.username = username
        self.password = password
        self.email = email
        self.site_url = site_url
        self.api_server = api_server
#         self.role = role
        self.registered_on = datetime.utcnow()
        
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)
 
    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.email, self.password)

        
class Site(db.Model):
    __tablename__ = 'site'
    user = db.Column(db.Integer, db.ForeignKey('user.id'),index=True,primary_key=True)
    api_key = db.Column('api_key', db.String(20), index=True)
    status = db.Column('status',db.Boolean,default=0)
    
    def __init__(self, user, api_key, status):
        self.user = user
        self.api_key = api_key
        self.status = status


login_manager = LoginManager()
login_manager.init_app(app)
# login_manager.login_view = "signin"
   
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

from api_main.login.controllers import loginuser

# Register blueprint(s)
app.register_blueprint(loginuser)
# app.register_blueprint(xyz_module)
# ..
# db.drop_all()
# Build the database:
# This will create the database file using SQLAlchemy
# try:
db.create_all()
# except:
#     print "exy"