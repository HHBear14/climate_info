from app import db, login, app2
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if password == '666666': return True  # remove after testing is done on website
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class z_cities(db.Model):
    #__searchable__ = ['city_id']  # these fields will be indexed by whoosh
    city_id=db.Column(db.Integer, primary_key=True)
    StateName=db.Column(db.String(64))
    MSAName=db.Column(db.String(64))
    UWHomes_AllTiers=db.Column(db.Float)
    UWHomes_TotalValue_AllTiers=db.Column(db.Float)
    AllHomes_AllTiers_ShareUW=db.Column(db.Float)



class Category(db.Model):
   category_id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(20))
   description = db.Column(db.String(600))


class Product(db.Model):
   product_id = db.Column(db.Integer, primary_key=True)
   category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'))
   name = db.Column(db.String(20))
   description = db.Column(db.String(600))
   image = db.Column(db.String(80))
   stock = db.Column(db.Integer)
   price = db.Column(db.Float)


class Kart(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Transaction(db.Model):
    t_id = db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    B_name=db.Column(db.String(40))
    B_email=db.Column(db.String(40))
    B_address=db.Column(db.String(70))
    B_city=db.Column(db.String(30))
    B_state=db.Column(db.String(15))
    B_zip=db.Column(db.Integer)
    P_NameonCard=db.Column(db.String(40))
    CC_number=db.Column(db.String(40))
    exp_month=db.Column(db.String(15))
    exp_year=db.Column(db.Integer)
    cvv=db.Column(db.Integer)
    sumtotal=db.Column(db.Float)
    reg_date=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class JoinTable(db.Model):
    j_id=db.Column(db.Integer, primary_key=True)
    t_id=db.Column(db.Integer, db.ForeignKey('transaction.t_id'))
    product_id=db.Column(db.Integer, db.ForeignKey("product.product_id"))
