# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, abort, Response, Markup
from flask_login import LoginManager, login_manager, login_required, logout_user, current_user
from flask_login.utils import login_user
from flask_sqlalchemy import SQLAlchemy
# from werkzeug import check_password_hash, generate_password_hash
from werkzeug.exceptions import default_exceptions
import json
import time
from api_main import db,User,Site
from pip._vendor.requests.packages.urllib3 import response
import requests
from flask.helpers import get_flashed_messages
from sqlalchemy.exc import IntegrityError
from wtforms import Form
from flask_wtf import form
import email

# Define the blueprint: 'auth', set its url prefix: app.url/auth
loginuser = Blueprint('auth', __name__, url_prefix='/auth')

# Set the route and accepted methods


@loginuser.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']    
#         user.role = "admin"
        user = User.query.filter_by(email=username).first()
#         if user.role == "admin":
        if user:
            if user.password == password:
                login_user(user)
                if user.id == 1:
                    return redirect('/auth/users')
                else:
                    return redirect('/auth/apis')
            else:
                return abort(401)
        else:
            return abort(401)
    return render_template("login.html")


@loginuser.route('/add_users', methods=['GET', 'POST'])
@login_required
def add_users():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']  
        email = request.form['email']
        site_url = request.form['site_url']
#         user = User.query.get(username)
        user = User.query.filter_by(username=username).all()
#         print user
        if user:
            flash('Duplicate Username detected')
        else:
            True
#         mail = User.query.get(email)
        mail = User.query.filter_by(email=email).all()
#         print mail
        if mail:
            flash('Duplicate Email detected')
        else:
            True
#         url = User.query.get(site_url)
        url = User.query.filter_by(site_url=site_url).all()
#         print url
        if url:
            flash('Duplicate URL detected')
        else:
            True
        try:
            site = User(username,password,email,site_url,'')
            db.session.add(site)
            db.session.commit()
            flash('User Successfully added')
        except TypeError:
            pass
        except IntegrityError:
            db.session.rollback()
#             flash('Duplicate entry detected')
    return render_template("add_users.html")


@loginuser.route('/add_pusers', methods=['GET', 'POST'])
@login_required
def add_pusers():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']  
        api_server = request.form['api_server']
        try:
            server = User(username,email,password,api_server)
            db.session.add(server)
            db.session.commit()
            flash('Partner User Successfully added')
        except TypeError:
            pass
        except IntegrityError:
            db.session.rollback()
            flash('Duplicate entry detected')
    return render_template("add_pusers.html")


@loginuser.route('/pusers', methods=['GET'])
@login_required
def pusers():
    return render_template("partner_users.html")

                
@loginuser.route('/users', methods=['GET'])
@login_required
def users():
    return render_template("list_users.html")


@loginuser.route('/apis', methods=['GET'])
@login_required
def apis():
    return render_template("list_apis.html")


@loginuser.route('/get_pusers',methods=['GET'])
@login_required
def partner_users():
    users = Puser.query.all()
    data = []
    for user in users:
        if user.id == 1:
            continue
        user_data = {} 
        user_data['id'] = user.id
        user_data['email'] = user.email
        user_data['api_server'] = user.api_server
        try:
            server = Server.query.get(user.id)
            user_data['status'] = server.status
        except AttributeError:
            user_data['status'] = False 
        data.append(user_data)
        final_data = {'data':data}
    return json.dumps(final_data)


@loginuser.route('/get_users',methods=['GET'])
@login_required
def list_users():
    users = User.query.all()
    data = []
    
    for user in users:
        if user.id == 1:
            continue
        user_data = {} 
        user_data['id'] = user.id
        user_data['email'] = user.email
        user_data['site_url'] = user.site_url
        user_data['details'] = True
        try:
            site = Site.query.get(user.id)
            user_data['status'] = site.status
        except AttributeError:
            user_data['status'] = False 
        data.append(user_data)
        
        final_data = {'data':data}
        
    return json.dumps(final_data)


@loginuser.route('/get_subscriber_details',methods=['POST'])
@login_required
def get_subscriber_details():
    token = request.form['token']
    userid = request.form['userid']
    site = Site.query.get(userid)
    api_key = site.api_key 
    partner_user = User.query.get(1)
    api_server = partner_user.api_server
    headers = {'Authorization': 'Bearer ' + token}
    response = requests.post(api_server+'/subscriber-details', data = {'api_key':api_key},headers=headers)
    return json.dumps(response.json())


@loginuser.route('/save_pdetails',methods=['POST'])
@login_required
def save_pdetails():
    status = request.form['status']
    apiserver = request.form['api_server']
    puserid = request.form['puserid']
#     print status,puserid,apiserver
    if status =="true":
        status = 1
    server = Server(api_server=apiserver,status=status,puser=puserid)
    db.session.add(server)
    db.session.commit()
    return Response('True')


@loginuser.route('/save_details',methods=['POST'])
@login_required
def save_details():
    status = request.form['status']
    apikey = request.form['api_key']
    userid = request.form['userid']
#     print status,userid,apikey
    if status =="true":
        status = 1
    site = Site(api_key=apikey,status=status,user=userid)
    db.session.add(site)
    db.session.commit()
    return Response('True')


@loginuser.route('/authenticate',methods=['GET'])
def authenticate():
    id = request.args.get('userid')
    site = Site.query.get(id)
    api_key = site.api_key
#     api_key = str(api_key)
#     print type(api_key)
#     print api_key
    partner_user = User.query.get(1)
    api_server = partner_user.api_server
    response = requests.post(api_server+'/authenticate', data = {'api_key':api_key})
    return json.dumps(response.json())
        

@loginuser.route('/get_api_server',methods=['GET'])
def get_current_api_server():
    id = request.args.get('userid')
    usr = User.query.get(id)
    api_server = usr.api_server
    data = {'api_server':api_server}
#     print api_server
    return json.dumps(data)


@loginuser.route('/token_invalidate',methods=['POST'])
@login_required
def invalidate():
    token = request.form['token']
    partner_user = User.query.get(1)
    api_server = partner_user.api_server
    headers = {'Authorization': 'Bearer ' + token}
    response = requests.delete(api_server+'/invalidate', headers=headers)
    return json.dumps(response.status_code)            


@loginuser.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/auth/signin')