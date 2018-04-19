from flask_login import LoginManager
from flask import Flask
from config import Config


app2 = Flask(__name__)
app2.config.from_object(Config)

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy(app2)
migrate = Migrate(app2, db)

login = LoginManager(app2)

from app import routes
from app import user_routes
from app import models