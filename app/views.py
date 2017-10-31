from flask import render_template, request, redirect, url_for, flash
import flask_login
from app import app, services, babel, forms
# from config import LANGUAGES


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


@app.route('/create', methods=['GET', 'POST'])
def create():
    form = forms.CreateTaskForm()
    if form.validate_on_submit():
        flash('Created!!!')
        return redirect(url_for('login'))

    if form.errors:
        flash(form.errors)

    return redirect(url_for('index'))


@app.route('/')
@app.route('/index')
@flask_login.login_required
def index():
    if flask_login.current_user.is_admin():
        return render_template('index_dispatcher.html')
    else:
        return render_template('index_driver.html')
