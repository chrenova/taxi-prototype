from flask import jsonify, make_response
import flask_login
from . import users_blueprint, services


@users_blueprint.route('/', methods=['GET'])
@flask_login.login_required
def users():
    all = services.find_active_users()
    return make_response(jsonify([u.to_json(flask_login.current_user) for u in all]), 200)
