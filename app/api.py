from flask import request, jsonify, make_response
import flask_login
from app import app, models, services


@app.route('/api/users', methods=['GET'])
@flask_login.login_required
def users():
    all = services.find_active_users()
    return make_response(jsonify([u.to_json(flask_login.current_user) for u in all]), 200)



'''
API:
GET /api/tasks
fetch list of tasks for current user
POST /api/tasks
create a new task
PUT /api/tasks/{task_identifier}/status
{'status': 'FINISHED'}
update status of a given task
PUT /api/tasks/{task_identifier}/comment
{'comment': 'comment'}
create a new comment for a given task
PUT /api/tasks/{task_identifier}/archived
{}
archive task
'''

@app.route('/api/tasks', methods=['GET'])
@flask_login.login_required
def tasks():
    all = services.find_active_tasks_for_user(flask_login.current_user)
    return make_response(jsonify([t.to_json(flask_login.current_user) for t in all]), 200)


@app.route('/api/future_tasks', methods=['GET'])
@flask_login.login_required
def future_tasks():
    all = services.find_future_tasks_for_user(flask_login.current_user)
    return make_response(jsonify([t.to_json(flask_login.current_user) for t in all]), 200)


@app.route('/api/tasks/<task_id>', methods=['GET'])
@flask_login.login_required
def get(task_id):
    task = services.get_task(task_id, flask_login.current_user)
    return make_response(jsonify(task.to_json(flask_login.current_user)), 200)


@app.route('/api/tasks', methods=['POST'])
@flask_login.login_required
def create_new_task():
    data = request.get_json()
    assigned_to = data.get('assigned_to') or None
    origin = data.get('origin')
    destination = data.get('destination')
    comment = data.get('comment')
    estimated_price = data.get('estimated_price') or None
    time_to_arrive = data.get('time_to_arrive') or None
    planned_at = data.get('planned_at') or None
    # TODO validate()

    services.create_task(
        created_by=flask_login.current_user,
        planned_at=planned_at,
        assigned_to_id=assigned_to,
        origin=origin,
        destination=destination,
        comments=comment,
        estimated_price=estimated_price,
        time_to_arrive=time_to_arrive
    )
    return make_response(jsonify(), 201)


@app.route('/api/tasks/<task_id>', methods=['POST'])
@flask_login.login_required
def update_task(task_id):
    data = request.get_json()
    assigned_to = data.get('assigned_to') or None
    origin = data.get('origin')
    destination = data.get('destination')
    status = data.get('status')
    comment = data.get('comment')
    estimated_price = data.get('estimated_price') or None
    real_price = data.get('real_price') or None
    time_to_arrive = data.get('time_to_arrive') or None
    planned_at = data.get('planned_at') or None
    # TODO validate()

    services.update_task(
        task_id=task_id,
        created_by=flask_login.current_user,
        planned_at=planned_at,
        assigned_to_id=assigned_to,
        origin=origin,
        destination=destination,
        status=status,
        comments=comment,
        estimated_price=estimated_price,
        real_price=real_price,
        time_to_arrive=time_to_arrive
    )
    return make_response(jsonify(), 201)


@app.route('/api/tasks/<task_id>/status/claimed', methods=['PUT'])
@flask_login.login_required
def update_task_status_claimed(task_id):
    data = request.get_json()
    #TODO validate
    services.update_task_status(flask_login.current_user, task_id, models.TaskStatus.CLAIMED, comment=data.get('comment'))
    return make_response(jsonify(), 200)


@app.route('/api/tasks/<task_id>/status/processing', methods=['PUT'])
@flask_login.login_required
def update_task_status_processing(task_id):
    data = request.get_json()
    #TODO validate
    services.update_task_status(flask_login.current_user, task_id, models.TaskStatus.PROCESSING, comment=data.get('comment'))
    return make_response(jsonify(), 200)


@app.route('/api/tasks/<task_id>/status/finished', methods=['PUT'])
@flask_login.login_required
def update_task_status_finished(task_id):
    data = request.get_json()
    #TODO validate
    services.update_task_status(flask_login.current_user, task_id, models.TaskStatus.FINISHED, comment=data.get('comment'), price=data.get('price'))
    return make_response(jsonify(), 200)


@app.route('/api/tasks/<task_id>/archived', methods=['PUT'])
@flask_login.login_required
def archive_task(task_id):
    services.update_task_set_archived(flask_login.current_user, task_id)
    return make_response(jsonify(), 200)


@app.route('/api/tasks/<task_id>/comment', methods=['PUT'])
@flask_login.login_required
def comment_task(task_id):
    data = request.get_json()
    if data and 'comment' in data:
        comment = data['comment']
        services.update_task_add_comment(flask_login.current_user, task_id, comment)
    return make_response(jsonify(), 200)


@app.route('/api/messages', methods=['GET'])
@flask_login.login_required
def get_messages():
    all = services.find_unseen_messages()
    json_response = jsonify([t.to_json() for t in all])
    services.update_messages_as_seen()
    return make_response(json_response, 200)


@app.route('/api/tasks/<task_id>/messages', methods=['POST'])
@flask_login.login_required
def create_new_message(task_id):
    data = request.get_json()
    created_by = flask_login.current_user
    message = data.get('message')
    services.create_message(created_by, task_id, message)
    # TODO: what if create_message failed???
    return make_response(jsonify(), 201)
