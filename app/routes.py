from app import app2 as app
from flask import render_template, redirect, url_for
from app.forms import LoginForm
from app.models import User, db, Z_Cities



@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/cities',methods=['GET', 'POST'])
def cities():
    form = Z_Cities()
    if form.search.data is not None:
        cities=Z_Cities.query.filter(Z_Cities.MSAName.like('%'+ form.search.data))
    else:
        return 'Your City was not found'
    #if request.method == 'POST' and form.validate_on_submit():
        #return redirect((url_for('search_results', query=form.search.data)))  # or what you want
    return render_template('cities.html', form=form, cities=cities)

@app.route('/searchResults/<int:city_id>/<string:from_page>')
def searchResults(city_id,from_page):
    if current_user.is_anonymous:
        return 'Please Login to see results'