from flask import Blueprint

tasks_blueprint = Blueprint('tasks', __name__)

from . import views, services
