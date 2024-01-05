from datetime import datetime

from flask import (
    render_template,
    flash,
    redirect,
    url_for,
    Blueprint,
    g, request, )
from flask_login import current_user
import core.post.logic as core_logic
from core.post.forms import PostForm
from core.post.models import Post
from core.user.models import Category, db

posts_bp = Blueprint('posts', __name__)


@posts_bp.before_request
def before_request():
    # Prevent Unauthorized Access
    if not current_user.is_authenticated:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('user.login_user'))
    g.user_id = current_user.id if current_user.is_authenticated else None
    g.categories = Category.query.filter_by(deleted_at=None).all()


@posts_bp.route('/posts')
@posts_bp.route('/post/<post_id>')
def retrieve_post(post_id=None):
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search_query', '')

    posts, template = core_logic.get_user_posts(g.user_id, post_id, page=page, search_query=search_query)

    if posts is None:
        flash('Invalid page number. Redirecting to the first page.', 'warning')
        return redirect(url_for('posts.retrieve_post'))

    data = {'user_id': g.user_id, 'posts': posts, 'search_query': search_query}
    return render_template(template, data=data)


@posts_bp.route('/post/create', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    form.user_id.data = g.user_id

    if form.validate_on_submit():
        try:
            core_logic.create_post(form.data)
            flash('Post created successfully!', 'success')
            return redirect(url_for('posts.retrieve_post'))
        except Exception as e:
            flash(f"Error creating post: {e}", 'error')
    elif form.errors:
        flash(f"Form validation errors: {form.errors}")

    data = {'categories': g.categories, 'user_id': g.user_id}
    return render_template('post/create.html', form=form, data=data)


@posts_bp.route('/post/<post_id>/update', methods=['GET', 'POST'])
def update_post(post_id):
    post = Post.query.filter_by(user_id=g.user_id, deleted_at=None, id=post_id).first()

    if not post:
        flash('Unauthorized access or Post not found.', 'error')
        return redirect(url_for('posts.retrieve_post'))

    data = {'categories': g.categories}
    form = PostForm(obj=post)
    form.is_update = True

    if form.validate_on_submit():
        try:
            core_logic.update_post(form.data, post)
            flash('Post updated successfully!', 'success')
            return redirect(url_for('posts.retrieve_post'))
        except Exception as e:
            flash(f"Error updating post: {e}", 'error')
    elif form.errors:
        flash(f"Form validation errors: {form.errors}")

    return render_template('post/update.html', form=form, data=data)


@posts_bp.route('/post/<post_id>/delete', methods=['GET'])
def delete_post(post_id):
    post = Post.query.filter_by(user_id=g.user_id, deleted_at=None, id=post_id).first()

    if not post:
        flash('Unauthorized access or Post not found.', 'error')
        return redirect(url_for('posts.retrieve_post'))

    try:
        post.deleted_at = datetime.utcnow()
        db.session.commit()
        flash('Post deleted successfully!', 'success')
    except Exception as e:
        flash(f"Error deleting post: {e}", 'error')

    return redirect(url_for('posts.retrieve_post'))
