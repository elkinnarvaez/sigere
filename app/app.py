from flask import Flask, Blueprint, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
import os, json, boto3
from werkzeug.utils import secure_filename
import requests
import psycopg2
from datetime import timedelta
import auth.auth as auth
import app.utils as utils

ALLOWED_FILE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.register_blueprint(auth.auth)
app.secret_key = '\xdb\x9d\xc6\x08\xe9\x1d\xaa\x7f\xe5\xd6\xfb\xf7\xcb]\x04\xd4c\x0f\xaf$\x83\xd5\x16\x94'
# app.permanent_session_lifetime = timedelta(days=2)
if(os.environ['DATABASE_URL'][0:10] == "postgresql"):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = utils.convert_uri(os.environ['DATABASE_URL'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
#     'connect_args': {'sslmode':'require'}
# }

RUNNING_LOCAL = os.environ['RUNNING_LOCAL']

db = SQLAlchemy(app)

# Tables definition
class Users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    names = db.Column(db.String(150))
    lastnames = db.Column(db.String(150))
    email = db.Column(db.String(150))
    username = db.Column(db.String(150))
    password = db.Column(db.String(150))
    job = db.Column(db.String(150))
    company = db.Column(db.String(150))
    city = db.Column(db.String(150))
    profile_picture = db.Column(db.String(800))

    def __init__(self, names, lastnames, email, username, password, job, company, city, profile_picture):
        self.names = names
        self.lastnames = lastnames
        self.email = email
        self.username = username
        self.password = password
        self.job = job
        self.company = company
        self.city = city
        self.profile_picture = profile_picture

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_FILE_EXTENSIONS

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.route('/home')
def home():
    args = dict()
    args["session"] = session
    return render_template("home.html", args = args)

@app.route('/')
def index():
    # session.permanent = True
    session["pre_login_email"] = None
    session["RUNNING_LOCAL"] = RUNNING_LOCAL
    session["email_username"] = None
    session["password"] = None
    return redirect(url_for("auth.login"))