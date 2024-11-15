from functools import wraps

from flask import Blueprint, render_template, redirect, url_for, session, request, current_app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.validators import ValidationError
from password_validator import PasswordValidator

import podcast.authentication.authentication_services as authentication_services
import podcast.adapters.repository as repo

authentication_blueprint = Blueprint('authentication_bp', __name__)


#need to link repo functionality

@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    repository = repo.repo_instance
    form = RegistrationForm()
    username_not_unique = None

    #checking if user had tried to submit the form
    if form.validate_on_submit():
        try:
            #attempt to add the user to the list of users in the repo
            #then redirect to login page if successful
            authentication_services.add_user(form.username.data, form.password.data, repository)
            return redirect(url_for('authentication_bp.login'))
        except authentication_services.NameNotUniqueException:
            username_not_unique = "There is already a user with this name, please choose a different one"

    #loading page initially (GET) or failed POST
    return render_template(
        'register.html',
        form=form,
        username_error_message=username_not_unique
    )


@authentication_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    repository = repo.repo_instance
    form = LoginForm()
    username_error_message = None
    password_error_message = None
    redirect_message = None
    if 'redirect_message' in session:
        redirect_message = session['redirect_message']
        session['redirect_message'] = None

    if form.validate_on_submit():
        try:
            user = authentication_services.get_user(form.username.data, repository)
            authentication_services.authenticate_user(user.username, form.password.data, repository)
            session.clear()
            session['username'] = user.username
            return redirect(url_for('home_bp.home'))
        except authentication_services.UnknownUserException:
            username_error_message = "Username unrecognised. Please try again."
        except authentication_services.AuthenticationException:
            password_error_message = "Password does not match. Please try again."

    return render_template('login.html',
                           form=form,
                           password_error_message=password_error_message,
                           username_error_message=username_error_message,
                           redirect_message=redirect_message
                           )


@authentication_blueprint.route('/logout')
def logout():
    repository = repo.repo_instance
    session.clear()
    return redirect(url_for('home_bp.home'))


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'username' not in session:
            session['redirect_message'] = "You must log in to post a review or create a playlist"
            return redirect(url_for('authentication_bp.login'))
        return view(**kwargs)
    return wrapped_view


class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = u'Your password must be at least 8 characters, and contain an upper case letter, \
                a lower case letter and a digit'
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .min(8) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    username = StringField('Username', [
        DataRequired(message='Your username is required'),
        Length(min=3, message='Your username is too short')])
    password = PasswordField('Password', [
        DataRequired(message='Your password is required'),
        PasswordValid()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', [
        DataRequired(message='Your log in information is required'),
    ])
    password = PasswordField('Password', [
        DataRequired(message='Your log in information is required'),
    ])
    submit = SubmitField('Login')
