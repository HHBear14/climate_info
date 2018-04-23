from app import db, login, app2
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_whooshalchemy import whoosh_index

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

#whoosh_index(app2, Z_Cities)