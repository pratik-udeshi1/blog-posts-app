from elasticsearch import Elasticsearch

from app import app
from core.post.models import Post

es = Elasticsearch(['http://localhost:9200'])

index_name = 'posts_index'

if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)

index_settings = {
    'mappings': {
        'properties': {
            'title': {'type': 'text'},
            'content': {'type': 'text'},
        }
    }
}

with app.app_context():
    es.indices.create(index=index_name, body=index_settings, ignore=[400])
    posts = Post.query.all()

    for post in posts:
        document = {
            'post_id': post.id,
            'title': post.title,
            'content': post.content,
        }

        # Index the document in Elasticsearch
        es.index(index=index_name, body=document)
        print(f"Index for Post {post.id} created successfully!!!")
    print(f"{len(posts)} Posts Indexed successfully!!!")
