from flask import flash
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from core.user.models import db


class GenericHttpHandler:
    @classmethod
    def handle_request(cls, request, form, **kwargs):
        if request.method == 'POST':
            return cls.post(request, form, **kwargs)
        else:
            return cls.retrieve_data(**kwargs)

    @classmethod
    def post(cls, request, form, **kwargs):
        try:
            if form.validate_on_submit():
                return cls.process_post(request, form, **kwargs)
            else:
                flash(f"Form validation errors: {form.errors}")
        except (IntegrityError, SQLAlchemyError) as e:
            cls.handle_database_errors(e)

        return cls.retrieve_data(**kwargs)

    @classmethod
    def get(cls, request, **kwargs):
        return cls.retrieve_data(**kwargs)

    @classmethod
    def retrieve_data(cls, **kwargs):
        raise NotImplementedError("Subclasses must implement the retrieve_data method.")

    @classmethod
    def process_post(cls, request, form, **kwargs):
        raise NotImplementedError("Subclasses must implement the process_post method.")

    @classmethod
    def handle_database_errors(cls, exception):
        db.session.rollback()
        print("Database Error---------->", str(exception))
        error_message = str(exception).split('[SQL:', 1)[0]
        flash(f'Database Error: {error_message}', 'error')
        return cls.retrieve_data()
