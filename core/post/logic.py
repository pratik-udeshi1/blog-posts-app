from flask_login import login_user, current_user
from flask_sqlalchemy.pagination import Pagination
from sqlalchemy import desc

from core.post.models import Post
from core.user.models import db, User


def get_mock_user():
    # Mocking User for Testing..
    test_user = User.query.join(Post).first()
    login_user(test_user)
    return current_user.id if current_user.is_authenticated else None


def get_user_posts(user_id, post_id=None, page=1, per_page=5):
    query = Post.query.filter_by(deleted_at=None)

    if post_id:
        post = query.filter_by(id=post_id).first()
        template = 'post/detail.html'
        return [post], template

    posts_query = query.order_by(desc('created_at'))

    # Corrected pagination without unnecessary argument
    paginated_posts = posts_query.paginate(page=page, per_page=per_page)

    template = 'post/all.html'
    return paginated_posts, template





def create_post(data):
    new_post = Post(**{key: value for key, value in data.items() if key != 'csrf_token'})
    db.session.add(new_post)
    db.session.commit()


def update_post(data, post):
    for key, value in data.items():
        setattr(post, key, value)
    db.session.commit()
