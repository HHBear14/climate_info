from app import app2 as app
from flask import render_template, redirect, url_for
from app.forms import LoginForm, CityForm
from app.models import User, db, z_cities
from flask import request
import pandas as pd
from fbprophet import Prophet
import matplotlib.pyplot as plt
import numpy as np
plt.interactive(True)



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

@app.route('/Co2')
def Co2():
    Co2 = pd.read_csv('climate_data/co2/co2-mm-mlo.csv')

    Co2.set_index('Date', inplace=True)
    Co2['ds'] = Co2.index
    Co2['y'] = Co2['Average']
    forecast_data = Co2[['ds', 'y']].copy()
    forecast_data.reset_index(inplace=True)
    del forecast_data['Date']

    m = Prophet(mcmc_samples=300, weekly_seasonality=False)
    m.add_seasonality(name='monthly', period=30.5, fourier_order=5)
    m.fit(forecast_data);

    future = m.make_future_dataframe(periods=998, freq='m')

    forecast = m.predict(future)
    forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_json()

    #fig = m.plot(forecast, xlabel='Date', ylabel='Co2 ppm').to_json
    #plt.title('Co2 in our Atmosphere')
    #fig.gca().yaxis.set_major_formatter(plt.show('${x:,.0f}'))

    #comp=m.plot_components(forecast).to_json

    return forecast