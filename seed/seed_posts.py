from faker import Faker
from sqlalchemy import func

from app import app
from core.post.models import Post
from core.user.models import Category, db

fake = Faker(app)


def generate_fake_post():
    with app.app_context():
        random_category = Category.query.order_by(func.random()).first()

    return Post(
        title=fake.sentence(),
        content=fake.paragraph(nb_sentences=100),
        user_id='70b33caa-0212-404f-bc81-313778e748c6',
        category_id=random_category.id if random_category else None
    )


def seed_posts(num_posts=500):
    posts = [generate_fake_post() for _ in range(num_posts)]

    with app.app_context():
        db.session.add_all(posts)
        db.session.commit()

        print(f"{num_posts} posts added successfully.")


if __name__ == '__main__':
    seed_posts()
