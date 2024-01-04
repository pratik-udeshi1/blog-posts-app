from flask import (
    render_template,
    flash,
    Blueprint, redirect, url_for,
)
from flask_login import login_user as flask_login_user, current_user, login_required, logout_user as flask_logout_user
from psycopg2 import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash

from core.user.forms import RegistrationForm, LoginForm
from core.user.logic import handle_database_errors
from core.user.models import db, User

user_bp = Blueprint('user', __name__)


@user_bp.route('/user/register', methods=['GET', 'POST'])
def register_user():
    form = RegistrationForm()
    try:
        if form.validate_on_submit():
            new_user = User()
            form.populate_obj(new_user)
            new_user.password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
            db.session.add(new_user)
            db.session.commit()
            flash('User added successfully!', 'success')
        elif form.errors:
            flash(f"Form validation errors: {form.errors}")
    except (IntegrityError, SQLAlchemyError) as db_exception:
        handle_database_errors(db_exception)

    return render_template('user/registration.html', form=form)


@user_bp.route('/user/login', methods=['GET', 'POST'])
def login_user():
    form = LoginForm()
    try:
        if form.validate_on_submit():
            user = User.query.filter_by(deleted_at=None, email=form.email.data).first()
            valid_password = check_password_hash(user.password, form.password.data)

            if user and valid_password:
                flask_login_user(user)
                flash('logged in successfully', 'success')
                return redirect(url_for('posts.retrieve_post'))
            else:
                flash('Email or Password is incorrect', 'error')
        elif form.errors:
            flash(f"Form validation errors: {form.errors}")
    except (IntegrityError, SQLAlchemyError) as db_exception:
        handle_database_errors(db_exception)

    if current_user.is_authenticated:
        return redirect(url_for('posts.retrieve_post'))

    return render_template('user/login.html', form=form)


@user_bp.route('/user/logout')
@login_required
def logout_user():
    flask_logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('user.login_user'))
