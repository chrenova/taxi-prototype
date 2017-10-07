from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_login
from flask_babel import Babel

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

babel = Babel(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

from app import views, models
