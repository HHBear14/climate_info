from app import app2 as app
from flask import render_template, redirect, url_for
from app.forms import LoginForm, CityForm
from app.models import User, db, z_cities
from flask import request



@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/cities',methods=['GET', 'POST'])
def cities():
    form = CityForm()

    #cities1=db.engine.execute("SELECT z_cities.MSAName FROM z_cities")


    return render_template('cities.html', form=form)

#@app.route('/searchResults/<int:city_id>/<string:from_page>')
#def searchResults(city_id,from_page):
   # form=CityForm()
    #if current_user.is_anonymous:
        #return 'Please Login to see results'
    #else:
        #form.validate_on_submit()
    #return render_template('cities.html')
@app.route('/search_results',methods=['GET', 'POST'])
def search_results():
    form = CityForm()
    if form.search.data is not None:
        results = z_cities.query.filter(z_cities.MSAName.like('%'+form.search.data))
        return render_template('search_results.html', results=results,form=form)
    else:
        results = db.engine.execute("SELECT z_cities.MSAName FROM z_cities")
        return render_template('cities.html', results=results, form=form)