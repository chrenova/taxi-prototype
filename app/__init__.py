import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_login
from flask_babel import Babel

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

babel = Babel(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

from .main import main_blueprint
app.register_blueprint(main_blueprint)
from .auth import auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')
from .messages import messages_blueprint
app.register_blueprint(messages_blueprint, url_prefix='/api/messages')
from .tasks import tasks_blueprint
app.register_blueprint(tasks_blueprint, url_prefix='/api/tasks')
from .users import users_blueprint
app.register_blueprint(users_blueprint, url_prefix='/api/users')
from .shifts import shifts_blueprint
app.register_blueprint(shifts_blueprint, url_prefix='/api/shifts')

from app import models
