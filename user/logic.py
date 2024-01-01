from flask import flash
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from werkzeug.security import generate_password_hash

from common.GenericHttpHandler import GenericHttpHandler
from user.models import User, db


class UserRegistration(GenericHttpHandler):

    @classmethod
    def retrieve_data(cls):
        return User.query.filter_by(deleted_at=None).order_by(desc('created_at')).all()

    @classmethod
    def post(cls, request, form):
        try:
            if form.validate_on_submit():
                new_user = User()
                form.populate_obj(new_user)
                new_user.password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
                # check_password_hash('pbkdf2-password-string', '1234') #To Check password while login..
                db.session.add(new_user)
                db.session.commit()
                flash('User added successfully!', 'success')
            else:
                flash(f"Form validation errors: {form.errors}")
        except (IntegrityError, SQLAlchemyError) as e:
            cls.handle_database_errors(e)

        return cls.retrieve_data()
