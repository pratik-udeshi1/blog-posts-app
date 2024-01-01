from flask import Blueprint, render_template, request

from core.user.forms import RegistrationForm, LoginForm
from core.user.views import UserRegistration, UserLogin

user_blueprint = Blueprint('user', __name__, url_prefix='/user')


@user_blueprint.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    registration_handler = UserRegistration()
    users = registration_handler.handle_request(request, form)
    return render_template('user/registration.html', form=form, users=users)


@user_blueprint.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    login_handler = UserLogin()
    users = login_handler.handle_request(request, form)
    return render_template('user/login.html', form=form)
