from datetime import datetime

from flask import render_template, flash, redirect, url_for, Blueprint, g
from psycopg2 import IntegrityError
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError

from core.post.forms import PostForm
from core.post.utils import get_mock_user
from core.user.models import Post, db, Category

posts_bp = Blueprint('posts', __name__)


@posts_bp.before_request
def before_request():
    # Mocking User for Testing..
    g.user_id = get_mock_user()
    g.categories = Category.query.filter_by(deleted_at=None).all()


@posts_bp.route('/posts')
@posts_bp.route('/post/<post_id>')
def retrieve_post(post_id=None):
    user_id = g.user_id
    query = Post.query.filter_by(deleted_at=None)

    if post_id:
        posts = query.filter_by(id=post_id).first()
        template = 'post/detail.html'
        if posts is None:
            flash('Post not found.', 'error')
            return redirect(url_for('posts.retrieve_post'))
    else:
        posts = query.filter_by(user_id=user_id).order_by(desc('created_at')).all()
        template = 'post/all.html'

    data = {'user_id': user_id, 'posts': posts}
    return render_template(template, data=data)


@posts_bp.route('/post/create', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    data = dict()
    data['categories'] = g.categories
    data['user_id'] = g.user_id
    try:
        if form.validate_on_submit():
            new_post = Post()
            form.populate_obj(new_post)
            db.session.add(new_post)
            db.session.commit()
            flash('Post created successfully!', 'success')
            return redirect(url_for('posts.retrieve_post'))
        elif form.errors:
            flash(f"Form validation errors: {form.errors}")
    except (IntegrityError, SQLAlchemyError) as e:
        flash(f"Database errors: {e}")

    return render_template('post/create.html', form=form, data=data)


@posts_bp.route('/post/<post_id>/update', methods=['GET', 'POST'])
def update_post(post_id):
    post = Post.query.filter_by(deleted_at=None, id=post_id).first()
    if post is None:
        flash('Post not found.', 'error')
        return redirect(url_for('posts.retrieve_post'))

    data = dict()
    data['categories'] = g.categories

    form = PostForm(obj=post)
    if form.validate_on_submit():
        form.populate_obj(post)
        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('posts.retrieve_post'))
    return render_template('post/update.html', form=form, data=data)


@posts_bp.route('/post/<post_id>/delete', methods=['GET'])
def delete_post(post_id):
    post = Post.query.filter_by(deleted_at=None, id=post_id).first()
    if post:
        post.deleted_at = datetime.utcnow()
        db.session.commit()
        flash('Post deleted successfully!', 'success')
    else:
        flash('Post not found.', 'error')
    return redirect(url_for('posts.retrieve_post'))
