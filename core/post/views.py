from flask import flash
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from core.common.GenericHttpHandler import GenericHttpHandler
from core.user.models import User, Post, db, Category


class UserPostShow(GenericHttpHandler):

    @classmethod
    # Retrieve all or single post for the user
    def retrieve_data(cls, user_id, post_id=None):
        if post_id:
            return Post.query.filter_by(id=post_id, user_id=user_id).first()

        user_query = User.query.filter_by(deleted_at=None, id=user_id)
        return user_query.order_by(desc('created_at')).first()

    @classmethod
    def post(cls, request, form=None, user_id=None):
        pass


class UserPostCreate(GenericHttpHandler):

    @classmethod
    # Retrieve all or single post for the user
    def retrieve_data(cls, user_id=None):
        data = dict()
        data['categories'] = Category.query.filter_by(deleted_at=None).all()
        data['user_id'] = user_id
        return data

    @classmethod
    def post(cls, request, form=None, user_id=None):
        try:
            if form.validate_on_submit():
                new_post = Post()
                form.populate_obj(new_post)
                db.session.add(new_post)
                db.session.commit()
                flash('Post Created successfully!', 'success')
            else:
                flash(f"Form validation errors: {form.errors}")
        except (IntegrityError, SQLAlchemyError) as e:
            cls.handle_database_errors(e)

        return cls.retrieve_data(user_id)
