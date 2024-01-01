from flask import flash
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from werkzeug.security import generate_password_hash

from core.common.GenericHttpHandler import GenericHttpHandler
from core.user.models import User, db


class UserDashboard(GenericHttpHandler):

    @classmethod
    def retrieve_data(cls, user_id):
        return User.query \
            .filter_by(deleted_at=None, id=user_id) \
            .order_by(desc('created_at')) \
            .first()

    @classmethod
    def post(cls, request, form=None, user_id=None):
        print("POST IS CALLED")
        return True
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

        return cls.retrieve_data(user_id)
