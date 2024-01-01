from flask import flash
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from common.GenericHttpHandler import GenericHttpHandler
from user.models import User, db


class UserRegistration(GenericHttpHandler):

    @classmethod
    def retrieve_data(cls):
        users = User.query.filter_by(deleted_at=None).order_by(desc('created_at')).all()
        return users

    @classmethod
    def post(cls, request, form, post_handler=None):
        try:
            if form.validate_on_submit():
                new_user = User()
                form.populate_obj(new_user)
                db.session.add(new_user)
                db.session.commit()
                flash('User added successfully!', 'success')
                return cls.retrieve_data()
            else:
                flash(f"Form validation errors: {form.errors}")
        except (IntegrityError, SQLAlchemyError) as e:
            return cls.handle_database_errors(e)

        return cls.retrieve_data()
