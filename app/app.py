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
app.permanent_session_lifetime = timedelta(hours=5)
if(os.environ['DATABASE_URL'][0:10] == "postgresql"):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = utils.convert_uri(os.environ['DATABASE_URL'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
#     'connect_args': {'sslmode':'require'}
# }

RUNNING_LOCAL = True if os.environ['RUNNING_LOCAL']=='yes' else False

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

@app.route('/index')
def index():
    args = dict()
    if("user" not in session or session["user"] == None):
        flash("Por favor inicie sesión.")
        return redirect(url_for("auth.login"))
    args["session"] = dict(session)
    return render_template("app/index.html", args = args)

@app.route('/')
def login_redirect():
    if("user" not in session):
        session["pre_login_email"] = None
        session["RUNNING_LOCAL"] = RUNNING_LOCAL
        session["user"] = None
    return redirect(url_for("auth.login"))

@app.route('/f404')
def f404():
    return render_template("app/404.html")

@app.route('/accordion')
def accordion():
    return render_template("app/accordion.html")

@app.route('/base')
def base():
    return render_template("app/base.html")

@app.route('/basic_table')
def basic_table():
    return render_template("app/basic-table.html")

@app.route('/bootstrap_ui')
def bootstrap_ui():
    return render_template("app/bootstrap-ui.html")

@app.route('/box_shadow')
def box_shadow():
    return render_template("app/box-shadow.html")

@app.route('/button')
def button():
    return render_template("app/button.html")

@app.route('/color')
def color():
    return render_template("app/color.html")

@app.route('/float_chart')
def float_chart():
    return render_template("app/float-chart.html")

@app.route('/forgot_password')
def forgot_password():
    return render_template("app/forgot-password.html")

@app.route('/form_elements_advance')
def form_elements_advance():
    return render_template("app/form-elements-advance.html")

@app.route('/form_elements_bootstrap')
def form_elements_bootstrap():
    return render_template("app/form-elements-bootstrap.html")

@app.route('/label_badge')
def label_badge():
    return render_template("app/label-badge.html")

@app.route('/light_box')
def light_box():
    return render_template("app/light-box.html")

@app.route('/login1')
def login1():
    return render_template("app/login1.html")

@app.route('/morris_chart')
def morris_chart():
    return render_template("app/morris-chart.html")

@app.route('/notification')
def notification():
    return render_template("app/notification.html")

@app.route('/panels_wells')
def panels_wells():
    return render_template("app/panels-wells.html")

@app.route('/register1')
def register1():
    return render_template("app/register1.html")

@app.route('/sample_page')
def sample_page():
    return render_template("app/sample-page.html")

@app.route('/tabs')
def tabs():
    return render_template("app/tabs.html")

@app.route('/tooltips')
def tooltips():
    return render_template("app/tooltips.html")

@app.route('/typography')
def typography():
    return render_template("app/typography.html")