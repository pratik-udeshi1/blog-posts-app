from flask import Flask
from flask_migrate import Migrate

from core.post.routes import post_blueprint
from core.user.models import db
from core.user.routes import user_blueprint

app = Flask(__name__, template_folder='core/templates')
app.config['SECRET_KEY'] = 'random_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/medium'

db.init_app(app)
migrate = Migrate(app, db, render_as_batch=True)

app.register_blueprint(user_blueprint)
app.register_blueprint(post_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
