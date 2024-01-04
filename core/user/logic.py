from flask import flash

from core.user.models import db


def handle_database_errors(exception):
    db.session.rollback()
    print("Database Error---------->", str(exception))
    error_message = str(exception).split('[SQL:', 1)[0]
    flash(f'Database Error: {error_message}', 'error')
    return True
