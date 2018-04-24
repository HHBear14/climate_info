from app import app2 as app
from flask import render_template, redirect, url_for, flash, request
from app.forms import LoginForm, CityForm
from app.models import User, db, z_cities, Product, Kart, Transaction, JoinTable, Category
from flask import request
import pandas as pd
from app import db
from fbprophet import Prophet
import matplotlib.pyplot as plt
import numpy as np
plt.interactive(True)
from flask_login import current_user



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

@app.route('/Co2button')
def Co2button():
    return render_template('Co2.html')

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
    future_json=future.to_json()

    forecast = m.predict(future)
    forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_json()

    #fig = m.plot(forecast, xlabel='Date', ylabel='Co2 ppm').to_json
    #plt.title('Co2 in our Atmosphere')
    #fig.gca().yaxis.set_major_formatter(plt.show('${x:,.0f}'))

    #comp=m.plot_components(forecast).to_json

    return forecast, future_json

@app.route('/Co2_dates')
def Co2_dates():
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
    future_json=future.to_json()

    forecast = m.predict(future)
    forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_json()

    #fig = m.plot(forecast, xlabel='Date', ylabel='Co2 ppm').to_json
    #plt.title('Co2 in our Atmosphere')
    #fig.gca().yaxis.set_major_formatter(plt.show('${x:,.0f}'))

    #comp=m.plot_components(forecast).to_json

    return future_json

@app.route('/products')
def products():
    product_list=Product.query.all()
    return render_template('products.html', products=product_list)

@app.route('/addToCart/<int:product_id>/<string:from_page>')
def addToCart(product_id, from_page):
    if current_user.is_anonymous:
        return redirect(url_for('login'))

    kart = Kart(user_id=current_user.id, product_id = product_id)
    db.session.add(kart)
    db.session.commit()
    return redirect(url_for('cart'))

@app.route('/removeFromCart/<int:product_id>/<string:from_page>')
def remove_cart(product_id,from_page):
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    kart=Kart.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    db.session.delete(kart)
    db.session.commit()
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    product_in_cart = Kart.query.filter_by(user_id=current_user.id).join(
        Product, Kart.product_id==Product.product_id).add_columns(
        Product.name, Product.price, Product.image, Product.product_id).all()
    #db.session.query(func.count().label('amount:')).all()

    return render_template('cart.html', products=product_in_cart, totalPrice=300, LoggedIn=current_user)

@app.route('/product/<string:product_id>')
def details(product_id):
    product_detail=Product.query.filter_by(product_id=product_id)
    return render_template('details.html', pDetail=product_detail)



@app.route('/checkout')
def checkout():

    if current_user.is_anonymous:
        return redirect(url_for('login'))
    product_in_cart = Kart.query.filter_by(user_id=current_user.id).join(
        Product, Kart.product_id==Product.product_id).add_columns(
        Product.name, Product.price, Product.image, Product.product_id).all()
    count = Kart.query.filter_by(user_id=current_user.id).count()
    sum1 = 0
    for product in product_in_cart:
        sum1 += product.price
    return render_template('checkout.html', products=product_in_cart, totalPrice=300, LoggedIn=current_user, sum=sum1, count=count)

@app.route('/checkout_action', methods=['POST'])
def checkout_action():

    #check name is correct

    #form1=CheckoutUserForm
    #form2=CheckoutBillingForm
    #if form1.validate_on_submit():

    #if form2.validate_on_submit():

    #cardname = request.form.get('card_name')
    #cardnumber = request.form.get('card_number')
    product_in_cart = Kart.query.filter_by(user_id=current_user.id).join(
        Product, Kart.product_id == Product.product_id).add_columns(
        Product.name, Product.price, Product.image, Product.product_id).all()
    sum1 = 0
    for product in product_in_cart:
        sum1 += product.price

    checkout_info = Transaction(user_id=current_user.id,B_name=request.form['firstname'], B_email=request.form['email'],B_address=request.form['address'],B_city=request.form['city'],B_state=request.form['state'],B_zip=request.form['zip'],P_NameonCard=request.form['cardname'],CC_number=request.form['cardnumber'],exp_month=request.form['expmonth'],exp_year=request.form['expyear'],cvv=request.form['cvv'],sumtotal=sum1)
    db.session.add(checkout_info)
    db.session.commit()

    for product in product_in_cart:
        receipt_info = JoinTable(product_id=product.product_id, t_id=checkout_info.t_id)
        db.session.add(receipt_info)
        db.session.commit()

    db.session.query(Kart).delete()
    db.session.commit()
    #remove selected items from Kart


    return render_template('checkout_action.html')