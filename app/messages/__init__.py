from flask import Blueprint

messages_blueprint = Blueprint('messages', __name__)

from . import views, services
