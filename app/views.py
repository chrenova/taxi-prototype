from flask import render_template, request, redirect, url_for, jsonify, make_response, flash
import flask_login
from app import app, models, services, babel, forms
from config import LANGUAGES


@babel.localeselector
def get_locale():
    # return request.accept_languages.best_match(LANGUAGES.keys())
    return 'sk'


'''
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
'''


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        u = services.valid_login(form.username.data, form.password.data)
        if u is not None:
            flask_login.login_user(u)
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.')

    if form.errors:
        flash(form.errors)

    return render_template('login.html', form=form, title='Login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        user = services.create_user(username=form.username.data, password=form.password.data, admin=form.admin.data, active=form.active.data)
        flash('You have successfully registered! You may now login.')

        return redirect(url_for('login'))

    if form.errors:
        flash(form.errors)

    return render_template('register.html', form=form, title='Register')


@app.route('/logout', methods=['GET', 'POST'])
@flask_login.login_required
def logout():
    flask_login.logout_user()
    flash('You have successfully been logged out.')
    return redirect(url_for('login'))


@app.route('/')
@app.route('/index')
@flask_login.login_required
def index():
    # all = models.Task.query.all()
    active_users = services.find_active_users()
    return render_template('index.html', active_users=active_users)


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


@app.route('/api/tasks', methods=['POST'])
@flask_login.login_required
def create_new_task():
    return make_response(jsonify(), 201)


@app.route('/create_task', methods=['POST'])
@flask_login.login_required
def create_task():
    assigned_to_id = request.form['assigned_to_id']
    assigned_to = services.find_user_by_id(int(assigned_to_id))
    origin = request.form['origin']
    destination = request.form['destination']
    comment = request.form['comment']
    estimated_price = request.form['estimated_price']
    time_to_arrive = request.form['time_to_arrive']
    planned_at = None  # FIXME
    services.create_task(
        created_by=flask_login.current_user,
        planned_at=planned_at,
        assigned_to=assigned_to,
        origin=origin,
        destination=destination,
        comments=comment,
        estimated_price=estimated_price,
        time_to_arrive=time_to_arrive
    )
    return redirect(url_for('index'))


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
