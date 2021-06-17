from flask import Flask, Blueprint, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
import os, json, boto3
from werkzeug.utils import secure_filename
import requests
import psycopg2
import auth.auth as auth
import app.utils as utils

ALLOWED_FILE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.register_blueprint(auth.auth)
app.secret_key = '\xdb\x9d\xc6\x08\xe9\x1d\xaa\x7f\xe5\xd6\xfb\xf7\xcb]\x04\xd4c\x0f\xaf$\x83\xd5\x16\x94'
if(os.environ['DATABASE_URL'][0:10] == "postgresql"):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = utils.convert_uri(os.environ['DATABASE_URL'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
#     'connect_args': {'sslmode':'require'}
# }

db = SQLAlchemy(app)

# Tables definition
class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    
    def __init__(self, name):
        self.name = name

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_FILE_EXTENSIONS

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.route('/')
def index():
    args = dict()
    return render_template("index.html", args = args)