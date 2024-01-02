from flask import Blueprint, render_template, request

from core.post.forms import PostForm
from core.post.views import UserPostShow, UserPostCreate

post_blueprint = Blueprint('post', __name__, url_prefix='/user')


@post_blueprint.route('<user_id>/posts', methods=['GET'])
@post_blueprint.route('<user_id>/post/<post_id>', methods=['GET'])
def show(user_id, post_id=None):
    post_handler = UserPostShow()
    user = post_handler.handle_request(request, form=None, user_id=user_id, post_id=post_id)

    if post_id:
        template = 'post/view.html'
    else:
        template = 'post/index.html'
    return render_template(template, user=user)


@post_blueprint.route('/<user_id>/post', methods=['POST', 'GET'])
def create(user_id=None):
    form = PostForm()
    post_handler = UserPostCreate()
    data = post_handler.handle_request(request, form, user_id=user_id)
    return render_template('post/create.html', form=form, data=data)
