from flask import Flask, render_template
from auth.auth import auth

app = Flask(__name__)
app.register_blueprint(auth)

print(auth.root_path)

@app.route('/')
def index():
  args = dict()
  args["msg"] = "Index page"
  return render_template("index.html", args = args)