from flask import flash, redirect, url_for
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash

from core.common.GenericHttpHandler import GenericHttpHandler
from core.user.models import User, db


class UserRegistration(GenericHttpHandler):

    @classmethod
    def retrieve_data(cls):
        pass
        # return User.query.filter_by(deleted_at=None).order_by(desc('created_at')).all()

    @classmethod
    def post(cls, request, form):
        try:
            if form.validate_on_submit():
                new_user = User()
                form.populate_obj(new_user)
                new_user.password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
                db.session.add(new_user)
                db.session.commit()
                flash('User added successfully!', 'success')
            else:
                flash(f"Form validation errors: {form.errors}")
        except (IntegrityError, SQLAlchemyError) as e:
            cls.handle_database_errors(e)

        return cls.retrieve_data()


class UserLogin(GenericHttpHandler):

    @classmethod
    def retrieve_data(cls):
        pass
        # return User.query.filter_by(deleted_at=None).order_by(desc('created_at')).all()

    @classmethod
    def post(cls, request, form):
        try:
            if form.validate_on_submit():
                user = User.query.filter_by(deleted_at=None, email=form.email.data).first()
                valid_password = check_password_hash(user.password, form.password.data)

                if user and valid_password:
                    flash('logged in successfully', 'success')
                    return redirect(url_for('dashboard'))  # Redirect to the 'dashboard' route
                else:
                    flash('Email or Password is incorrect', 'error')
            else:
                flash(f"Form validation errors: {form.errors}")
        except (IntegrityError, SQLAlchemyError) as e:
            cls.handle_database_errors(e)

        return cls.retrieve_data()
