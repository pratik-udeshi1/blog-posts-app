from flask import flash
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from user.models import db


class GenericHttpHandler:
    @classmethod
    def handle_request(cls, request, form):
        if request.method == 'POST':
            return cls.post(request, form)
        else:
            return cls.retrieve_data()

    @classmethod
    def post(cls, request, form, post_handler=None):
        try:
            if form.validate_on_submit():
                if post_handler:
                    return post_handler(request, form)
                else:
                    flash('No POST handler specified.', 'error')
            else:
                flash(f"Form validation errors: {form.errors}")

        except IntegrityError as e:
            db.session.rollback()
            flash('IntegrityError Error.', str(e))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash('SQLAlchemyError.', str(e))

        return cls.retrieve_data()

    @classmethod
    def get(cls, request, get_handler=None):
        if get_handler:
            return get_handler(request)
        else:
            flash('No GET handler specified.', 'error')
            return cls.retrieve_data()

    @classmethod
    def retrieve_data(cls):
        raise NotImplementedError("Subclasses must implement the retrieve_data method.")

    # Utility function to handle database errors
    @classmethod
    def handle_database_errors(cls, exception):
        db.session.rollback()
        error_message = str(exception).split('[SQL:', 1)[0]  # Split at the first colon and take the second part
        flash(f'Database Error: {error_message}', 'error')
        return cls.retrieve_data()  # Will now call the subclass's implementation
