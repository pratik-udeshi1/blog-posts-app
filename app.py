import flask_login
from flask import Flask
from flask_migrate import Migrate

from core.post.views import posts_bp
from core.user.models import db, User

app = Flask(__name__, template_folder='core/templates')

app.config['SECRET_KEY'] = 'random_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/medium'

login_manager = flask_login.LoginManager(app)
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


db.init_app(app)
migrate = Migrate(app, db, render_as_batch=True)

app.register_blueprint(posts_bp)

if __name__ == '__main__':
    app.run(debug=True)
