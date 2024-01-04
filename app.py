import flask_login
from flask import Flask, render_template, request, url_for
from flask_migrate import Migrate

from core.post.views import posts_bp
from core.user.models import db, User
from core.user.views import user_bp

app = Flask(__name__, template_folder='core/templates')

app.config['SECRET_KEY'] = 'random_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/medium'

login_manager = flask_login.LoginManager(app)
login_manager.login_view = 'login'
login_manager.init_app(app)


@app.errorhandler(404)
def not_found(error):
    previous_page = request.referrer
    if previous_page:
        return render_template('404.html', previous_page=previous_page)
    else:
        # If no referrer is available, redirect to the homepage
        return render_template('404.html', previous_page=url_for('posts.retrieve_post'))


@app.errorhandler(401)
def unauthorized(error):
    return render_template('401.html', previous_page=url_for('user.login_user'))


@login_manager.user_loader
def load_user(user_id):
    with db.session() as session:
        return session.get(User, user_id)


db.init_app(app)
migrate = Migrate(app, db, render_as_batch=True)

app.register_blueprint(user_bp)
app.register_blueprint(posts_bp)

if __name__ == '__main__':
    app.run(debug=True)
