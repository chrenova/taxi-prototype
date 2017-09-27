from flask import render_template, request, redirect, url_for, jsonify
import flask_login
from app import app, models, services


@app.route('/')
@app.route('/index')
@flask_login.login_required
def index():
    # all = models.Task.query.all()
    active_users = services.find_active_users()
    return render_template('index.html', active_users=active_users)


@app.route('/tasks')
@flask_login.login_required
def tasks():
    all = services.find_active_tasks_for_user(flask_login.current_user)
    return jsonify([t.to_json() for t in all])


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    user = services.valid_login(request.form['username'], request.form['password'])
    if user is not None:
        flask_login.login_user(user)
        return redirect(url_for('index'))
    else:
        return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    flask_login.logout_user()
    return redirect(url_for('login'))


@app.route('/create_task', methods=['POST'])
@flask_login.login_required
def create_task():
    assigned_to_id = request.form['assigned_to_id']
    assigned_to = services.find_user_by_id(int(assigned_to_id))
    origin = request.form['origin']
    destination = request.form['destination']
    comment = request.form['comment']
    services.create_task(created_by=flask_login.current_user, assigned_to=assigned_to, origin=origin, destination=destination, comments=comment)
    return redirect(url_for('index'))


@app.route('/start_progress/<task_id>', methods=['POST'])
@flask_login.login_required
def start_progress(task_id):
    services.update_task_set_processing(flask_login.current_user, task_id)
    return redirect(url_for('index'))


@app.route('/finish_task/<task_id>', methods=['POST'])
@flask_login.login_required
def finish_task(task_id):
    services.update_task_set_finished(flask_login.current_user, task_id)
    return redirect(url_for('index'))


@app.route('/archive_task/<task_id>', methods=['POST'])
@flask_login.login_required
def archive_task(task_id):
    services.update_task_set_archived(flask_login.current_user, task_id)
    return redirect(url_for('index'))
