from flask_login import login_user, current_user
from sqlalchemy import desc

from core.user.models import db, User
from core.post.models import Post


def get_mock_user():
    # Mocking User for Testing..
    test_user = User.query.join(Post).first()
    login_user(test_user)
    return current_user.id if current_user.is_authenticated else None


def get_user_posts(user_id, post_id=None):
    query = Post.query.filter_by(deleted_at=None)

    if post_id:
        posts = query.filter_by(id=post_id).first()
        template = 'post/detail.html'
    else:
        posts = query.order_by(desc('created_at')).all()
        template = 'post/all.html'

    return posts, template


def create_post(data):
    new_post = Post(**{key: value for key, value in data.items() if key != 'csrf_token'})
    db.session.add(new_post)
    db.session.commit()


def update_post(data, post):
    for key, value in data.items():
        setattr(post, key, value)
    db.session.commit()
