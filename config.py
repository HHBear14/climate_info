import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'Dov Only'

    SQLALCHEMY_DATABASE_URI = 'mysql://root:aaaaaa@localhost/climate_info'

    SQLALCHEMY_TRACK_MODIFICATIONS = False