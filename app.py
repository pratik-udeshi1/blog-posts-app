from flask import Flask
from flask_migrate import Migrate

from user.models import db
from user.routes import user_blueprint  # Import blueprint after app initialization

app = Flask(__name__)
app.config['SECRET_KEY'] = 'random_key'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/medium'

db.init_app(app)
migrate = Migrate(app, db, render_as_batch=True)

app.register_blueprint(user_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
