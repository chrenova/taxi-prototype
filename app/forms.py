from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, BooleanField, IntegerField, DecimalField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo

from app.models import User


class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    username = StringField('Username', validators=[DataRequired()])
    # first_name = StringField('First Name', validators=[DataRequired()])
    # last_name = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    admin = BooleanField('Administrator')
    active = BooleanField('Active')
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use.')


class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    # email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class CreateTaskForm(FlaskForm):
    assigned_to = SelectField('AssignedTo', coerce=int)
    # assigned_to = services.find_user_by_id(int(assigned_to_id))
    origin = StringField('Origin')
    destination = StringField('Destination')
    comment = StringField('Comment')
    estimated_price = DecimalField('EstimatedPrice')
    time_to_arrive = IntegerField('TimeToArrive')
    planned_at = None  # FIXME
    submit = SubmitField('Create')
