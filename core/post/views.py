from datetime import datetime

from flask import (
    render_template,
    flash,
    redirect,
    url_for,
    Blueprint,
    g,
)

import core.post.logic as core_logic
from core.post.forms import PostForm
from core.user.models import Category, Post, db

posts_bp = Blueprint('posts', __name__)


@posts_bp.before_request
def before_request():
    g.user_id = core_logic.get_mock_user()
    g.categories = Category.query.filter_by(deleted_at=None).all()


@posts_bp.route('/posts')
@posts_bp.route('/post/<post_id>')
def retrieve_post(post_id=None):
    posts, template = core_logic.get_user_posts(g.user_id, post_id)

    if not posts:
        flash('Post not found.', 'error')
        return redirect(url_for('posts.retrieve_post'))

    data = {'user_id': g.user_id, 'posts': posts}
    return render_template(template, data=data)


@posts_bp.route('/post/create', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    data = {'categories': g.categories, 'user_id': g.user_id}

    if form.validate_on_submit():
        try:
            core_logic.create_post(form.data, g.user_id)
            flash('Post created successfully!', 'success')
            return redirect(url_for('posts.retrieve_post'))
        except Exception as e:
            flash(f"Error creating post: {e}", 'error')

    return render_template('post/create.html', form=form, data=data)


@posts_bp.route('/post/<post_id>/update', methods=['GET', 'POST'])
def update_post(post_id):
    post = Post.query.filter_by(deleted_at=None, id=post_id).first()

    if not post:
        flash('Post not found.', 'error')
        return redirect(url_for('posts.retrieve_post'))

    data = {'categories': g.categories}
    form = PostForm(obj=post)

    if form.validate_on_submit():
        try:
            core_logic.update_post(form.data, post)
            flash('Post updated successfully!', 'success')
            return redirect(url_for('posts.retrieve_post'))
        except Exception as e:
            flash(f"Error updating post: {e}", 'error')

    return render_template('post/update.html', form=form, data=data)


@posts_bp.route('/post/<post_id>/delete', methods=['GET'])
def delete_post(post_id):
    post = Post.query.filter_by(deleted_at=None, id=post_id).first()

    if post:
        try:
            post.deleted_at = datetime.utcnow()
            db.session.commit()
            flash('Post deleted successfully!', 'success')
        except Exception as e:
            flash(f"Error deleting post: {e}", 'error')

    return redirect(url_for('posts.retrieve_post'))
