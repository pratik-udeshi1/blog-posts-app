from flask_login import login_user, current_user

from core.user.models import User, Post


def get_mock_user():
    # Mocking User for Testing..
    test_user = User.query.join(Post).first()
    login_user(test_user)
    user = current_user.id if current_user.is_authenticated else None
    return user
