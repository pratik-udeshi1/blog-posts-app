from flask import Blueprint, render_template, request

from user.forms import RegistrationForm
from user.logic import UserRegistration

user_blueprint = Blueprint('user', __name__, url_prefix='/user')


@user_blueprint.route('/register', methods=['POST', 'GET'])
def signup():
    form = RegistrationForm()
    registration_handler = UserRegistration()
    users = registration_handler.handle_request(request, form)
    return render_template('registration.html', form=form, users=users)
