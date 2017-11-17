from flask import jsonify, make_response, request
import flask_login
from . import tasks_blueprint, services as task_services
from ..users import services as users_services
from app.models import Task, TaskStatus


@tasks_blueprint.route('/', methods=['GET'])
@flask_login.login_required
def tasks():
    users_services.ping(flask_login.current_user)
    all = task_services.find_active_tasks_for_user(flask_login.current_user)
    return make_response(jsonify([t.to_json(flask_login.current_user) for t in all]), 200)


@tasks_blueprint.route('/next_days', methods=['GET'])
@flask_login.login_required
def future_tasks():
    all = task_services.find_future_tasks_for_user(flask_login.current_user)
    return make_response(jsonify([t.to_json(flask_login.current_user) for t in all]), 200)


@tasks_blueprint.route('/<int:task_id>', methods=['GET'])
@flask_login.login_required
def get(task_id):
    task = task_services.get_task(task_id, flask_login.current_user)
    return make_response(jsonify(task.to_json(flask_login.current_user)), 200)


@tasks_blueprint.route('/', methods=['POST'])
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

    task_services.create_task(
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


@tasks_blueprint.route('/<int:task_id>', methods=['POST'])
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

    task_services.update_task(
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


@tasks_blueprint.route('/<int:task_id>/status/claimed', methods=['PUT'])
@flask_login.login_required
def update_task_status_claimed(task_id):
    data = request.get_json()
    #TODO validate
    task_services.update_task_status(flask_login.current_user, task_id, TaskStatus.CLAIMED, comment=data.get('comment'))
    return make_response(jsonify(), 200)


@tasks_blueprint.route('/<int:task_id>/status/processing', methods=['PUT'])
@flask_login.login_required
def update_task_status_processing(task_id):
    data = request.get_json()
    #TODO validate
    task_services.update_task_status(flask_login.current_user, task_id, TaskStatus.PROCESSING, comment=data.get('comment'))
    return make_response(jsonify(), 200)


@tasks_blueprint.route('/<int:task_id>/status/finished', methods=['PUT'])
@flask_login.login_required
def update_task_status_finished(task_id):
    data = request.get_json()
    #TODO validate
    task_services.update_task_status(flask_login.current_user, task_id, TaskStatus.FINISHED, comment=data.get('comment'), price=data.get('price'))
    return make_response(jsonify(), 200)


@tasks_blueprint.route('/<int:task_id>/archived', methods=['PUT'])
@flask_login.login_required
def archive_task(task_id):
    task_services.update_task_set_archived(flask_login.current_user, task_id)
    return make_response(jsonify(), 200)


@tasks_blueprint.route('/<int:task_id>/comment', methods=['PUT'])
@flask_login.login_required
def comment_task(task_id):
    data = request.get_json()
    if data and 'comment' in data:
        comment = data['comment']
        task_services.update_task_add_comment(flask_login.current_user, task_id, comment)
    return make_response(jsonify(), 200)
