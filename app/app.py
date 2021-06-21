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
    return render_template("app/index.html", args = args, title='Inicio')

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
    args = dict()
    args["session"] = dict(session)
    return render_template("app/accordion.html", args = args)

@app.route('/base')
def base():
    args = dict()
    args["session"] = dict(session)
    return render_template("app/base.html", args = args)

@app.route('/basic_table')
def basic_table():
    args = dict()
    args["session"] = dict(session)
    return render_template("app/basic-table.html", args = args)

@app.route('/bootstrap_ui')
def bootstrap_ui():
    args = dict()
    args["session"] = dict(session)
    return render_template("app/bootstrap-ui.html", args = args)

@app.route('/box_shadow')
def box_shadow():
    args = dict()
    args["session"] = dict(session)
    return render_template("app/box-shadow.html", args = args)

@app.route('/button')
def button():
    args = dict()
    args["session"] = dict(session)
    return render_template("app/button.html", args = args)

@app.route('/color')
def color():
    args = dict()
    args["session"] = dict(session)
    return render_template("app/color.html", args = args)

@app.route('/float_chart')
def float_chart():
    args = dict()
    args["session"] = dict(session)
    return render_template("app/float-chart.html", args = args)

@app.route('/forgot_password')
def forgot_password():
    args = dict()
    args["session"] = dict(session)
    return render_template("app/forgot-password.html", args = args)

@app.route('/form_elements_advance')
def form_elements_advance():
    args = dict()
    args["session"] = dict(session)
    return render_template("app/form-elements-advance.html", args = args)

@app.route('/form_elements_bootstrap')
def form_elements_bootstrap():
    args = dict()
    args["session"] = dict(session)
    return render_template("app/form-elements-bootstrap.html", args = args)

@app.route('/label_badge')
def label_badge():
    args = dict()
    args["session"] = dict(session)
    return render_template("app/label-badge.html", args = args)

@app.route('/light_box')
def light_box():
    args = dict()
    args["session"] = dict(session)
    return render_template("app/light-box.html", args = args)

@app.route('/login1')
def login1():
    args = dict()
    args["session"] = dict(session)
    return render_template("app/login1.html", args = args)

@app.route('/morris_chart')
def morris_chart():
    args = dict()
    args["session"] = dict(session)
    return render_template("app/morris-chart.html", args = args)

@app.route('/notification')
def notification():
    args = dict()
    args["session"] = dict(session)
    return render_template("app/notification.html", args = args)

@app.route('/panels_wells')
def panels_wells():
    args = dict()
    args["session"] = dict(session)
    return render_template("app/panels-wells.html", args = args)

@app.route('/register1')
def register1():
    args = dict()
    args["session"] = dict(session)
    return render_template("app/register1.html", args = args)

@app.route('/sample_page')
def sample_page():
    args = dict()
    args["session"] = dict(session)
    return render_template("app/sample-page.html", args = args)

@app.route('/tabs')
def tabs():
    args = dict()
    args["session"] = dict(session)
    return render_template("app/tabs.html", args = args)

@app.route('/tooltips')
def tooltips():
    args = dict()
    args["session"] = dict(session)
    return render_template("app/tooltips.html", args = args)

@app.route('/typography')
def typography():
    args = dict()
    args["session"] = dict(session)
    return render_template("app/typography.html", args = args)

@app.route('/profile')
def profile():
    args = dict()
    args["session"] = dict(session)
    return render_template("app/profile.html", args = args, title="Perfil")

@app.route('/my_projects')
def my_projects():
    args = dict()
    args["session"] = dict(session)
    return render_template("app/my_projects.html", args = args, title="Mis proyectos")

@app.route('/projects_collaborator')
def projects_collaborator():
    args = dict()
    args["session"] = dict(session)
    return render_template("app/projects_collaborator.html", args = args, title="Proyectos como colaborador")

@app.route('/projects_stakeholder')
def projects_stakeholder():
    args = dict()
    args["session"] = dict(session)
    return render_template("app/projects_stakeholder.html", args = args, title="Proyectos como stakeholder")

@app.route('/deleted_projects')
def deleted_projects():
    args = dict()
    args["session"] = dict(session)
    return render_template("app/deleted_projects.html", args = args, title="Proyectos eliminados")

@app.route('/project_1')
def project_1():
    args = dict()
    args["session"] = dict(session)
    return render_template("app/project_1.html", args = args, title="SIGERE")


@app.route('/project_1/versions')
def versions():
    args = dict()
    args["session"] = dict(session)
    return render_template("app/versions.html", args = args, title="SIGERE")