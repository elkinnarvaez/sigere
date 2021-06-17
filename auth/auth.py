from flask import Blueprint, render_template

auth = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates', static_folder='static')

@auth.route('/login')
def login():
    args = dict()
    return render_template("auth/login.html", args = args)