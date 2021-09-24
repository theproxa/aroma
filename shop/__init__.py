from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import *


from config import Config

app = Flask(__name__)
db = SQLAlchemy(app)

app.config.from_object(Config)

migrate = Migrate(app,db)
login_manager = LoginManager(app)
login_manager.logim_view = 'login'

from shop import routs , models