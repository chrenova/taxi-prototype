from flask import request, jsonify, make_response
import flask_login
from . import shifts_blueprint, services


@shifts_blueprint.route('/', methods=['POST'])
@flask_login.login_required
def start_new_shift():
    # data = request.get_json()
    user = flask_login.current_user
    services.start_new_shift(user)
    # TODO: what if create_message failed???
    return make_response(jsonify(), 201)
