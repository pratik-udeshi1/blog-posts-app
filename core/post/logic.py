from elasticsearch import Elasticsearch
from flask_login import login_user, current_user
from sqlalchemy import desc

from core.post.es_search_queries import *
from core.post.models import Post
from core.user.models import db, User

es = Elasticsearch(['http://localhost:9200'])


def get_mock_user():
    # Mocking User for Testing..
    test_user = User.query.join(Post).first()
    login_user(test_user)
    return current_user.id if current_user.is_authenticated else None


def get_user_posts(user_id=None, post_id=None, page=1, per_page=5, search_query=None):
    query = Post.query.filter_by(deleted_at=None)

    if post_id:
        post = query.filter_by(id=post_id).first()
        template = 'post/detail.html'
        return post, template

    if search_query:
        query = get_posts_from_es(search_query)

    paginated_posts = query.paginate(page=page, per_page=per_page)
    template = 'post/all.html'
    return paginated_posts, template


def get_posts_from_es(search_query):
    query = Post.query.filter_by(deleted_at=None)
    es_query = es.search(index='posts_index', body=custom_search_query2(search_query))
    es_result_ids = [hit['_source']['post_id'] for hit in es_query['hits']['hits']]
    query = query.filter(Post.id.in_(es_result_ids))
    query = query.order_by(desc('created_at'))

    return query


def create_post(data):
    new_post = Post(**{key: value for key, value in data.items() if key != 'csrf_token'})
    db.session.add(new_post)
    db.session.commit()


def update_post(data, post):
    for key, value in data.items():
        setattr(post, key, value)
    db.session.commit()
