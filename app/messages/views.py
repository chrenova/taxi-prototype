from flask import request, jsonify, make_response
import flask_login
from . import messages_blueprint, services


@messages_blueprint.route('/', methods=['GET'])
@flask_login.login_required
def get_messages():
    all = services.find_unseen_messages()
    json_response = jsonify([t.to_json() for t in all])
    services.update_messages_as_seen()
    return make_response(json_response, 200)


@messages_blueprint.route('/tasks/<int:task_id>', methods=['POST'])
@flask_login.login_required
def create_new_message(task_id):
    data = request.get_json()
    created_by = flask_login.current_user
    message = data.get('message')
    services.create_message(created_by, task_id, message)
    # TODO: what if create_message failed???
    return make_response(jsonify(), 201)
