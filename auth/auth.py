from flask import Flask, Blueprint, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
import os, json, boto3
from werkzeug.utils import secure_filename
import requests
import psycopg2
import app.app as app

auth = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates', static_folder='static')

@auth.route('/logout', methods=["POST", "GET"])
def logout():
    session["user"] = None
    return redirect(url_for("auth.login"))

@auth.route('/login', methods=["POST", "GET"])
def login():
    args = dict()
    if request.method == "POST":
        if(request.form["signin"] == "Entrar"):
            email_username = request.form["email_username"]
            password = request.form["password"]
            remember_me = "remember_me" in request.form
            if(remember_me):
                session.permanent = True
            else:
                session.permanent = False
            user = app.Users.query.filter((app.Users.password == password) & ((app.Users.email == email_username) | (app.Users.username == email_username))).first()
            if(user != None):
                session['user'] = {
                    'names': user.names, 
                    'lastnames': user.lastnames,
                    'email': user.email,
                    'username': user.username,
                    'password': user.password,
                    'job': user.job,
                    'company': user.company,
                    'city': user.city,
                    'profile_picture': user.profile_picture
                    }
            else:
                flash("Las credenciales son invalidas.")
    if("user" in session and session["user"] != None):
        return redirect(url_for("index"))
    args["session"] = dict(session)
    return render_template("auth/login.html", args = args)

@auth.route('/signup', methods=["POST", "GET"])
def signup():
    args = dict()
    if request.method == "POST":
        if(request.form["signup"] == "Registrarse"):
            names = request.form["names"]
            lastnames = request.form["lastnames"]
            email = request.form["email"]
            username = request.form["username"]
            password = request.form["password"]
            repeated_password = request.form["repeated_password"]
            job = request.form["job"]
            company = request.form["company"]
            city = request.form["city"]
            user1 = app.Users.query.filter(app.Users.email == email).first()
            user2 = app.Users.query.filter(app.Users.username == username).first()
            add_user = True
            if(user1 != None or user2 != None):
                flash("El usuario ya se encuentra registrado.")
                add_user = False
            if(password != repeated_password):
                flash("Las contraseñas ingresadas no coinciden.")
                add_user = False
            if(names == "" or lastnames == "" or email == "" or username == "" or password == "" or repeated_password == "" or job == "" or company == "" or city == ""):
                flash("Algunos campos faltantes.")
                add_user = False
            if(add_user):
                session["pre_login_email"] = email
                DEFAULT_PROFILE_PICTURE = f"https://{os.environ.get('S3_BUCKET_NAME')}.s3.amazonaws.com/profile-pictures/avatar.png"
                new_user = app.Users(names, lastnames, email, username, password, job, company, city, DEFAULT_PROFILE_PICTURE)
                app.db.session.add(new_user)
                app.db.session.commit()
                flash("Te has registrado satisfactoriamente.")
                return redirect(url_for("auth.login"))
    if("user" in session and session["user"] != None):
        return redirect(url_for("index"))
    args["session"] = dict(session)
    return render_template("auth/signup.html", args = args)