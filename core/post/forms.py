from flask import current_app
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired

from core.user.models import Category


class PostForm(FlaskForm):
    id = StringField('Title', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    user_id = StringField('user_id', validators=[DataRequired()])
    category_id = SelectField('Category', choices=[], coerce=str, validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        # Dynamically populate category choices from the database
        with current_app.app_context():
            self.category_id.choices = [(category.id, category.name) for category in Category.query.all()]
