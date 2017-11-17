from flask import Blueprint

shifts_blueprint = Blueprint('shifts', __name__)

from . import views, services
