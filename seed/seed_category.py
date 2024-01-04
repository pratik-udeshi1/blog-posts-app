from app import app
from core.user.models import db, Category


def generate_fake_category():
    categories = [
        'Music', 'Technology', 'Space', 'Food', 'Travel', 'Fashion',
        'Health', 'Science', 'Art', 'Sports', 'Movies', 'Books',
        'Gaming', 'Fitness', 'History', 'Nature', 'Business', 'Education',
        'Photography', 'Cooking', 'DIY', 'Politics', 'Cars', 'Pets',
        'Parenting', 'Crafts', 'Humor', 'Home Decor'
    ]

    return categories


def seed_categories():
    get_categories = generate_fake_category()

    categories = [Category(name=get_categories[x]) for x in range(len(get_categories))]

    with app.app_context():
        db.session.add_all(categories)
        db.session.commit()

        print(f"{len(get_categories)} categories added successfully.")


if __name__ == '__main__':
    seed_categories()
