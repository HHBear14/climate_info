from app import app2 as app
from flask import render_template, redirect, url_for
from app.forms import LoginForm
from app.models import User, db


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')