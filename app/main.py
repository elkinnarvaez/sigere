from flask import Flask

app= Flask(__name__)

@app.route('/')
def index():
  return "Ok"

@app.route('/root')
def root():
  return "Elkin tiene novia"

@app.route('/reyes')
def reyes():
  return "jejeje"

@app.route('/elkin')
def elkin():
  return "Elkin"