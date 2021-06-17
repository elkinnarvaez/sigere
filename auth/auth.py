from flask import Flask, Blueprint, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
import os, json, boto3
from werkzeug.utils import secure_filename
import requests
import psycopg2
# import app.app as app

auth = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates', static_folder='static')

@auth.route('/login')
def login():
    args = dict()
    # new_user = app.users("Elkin")
    # app.db.session.add(new_user)
    # app.db.session.commit()
    return render_template("auth/login.html", args = args)