from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    content = TextAreaField('content', validators=[DataRequired()])
    user_id = StringField('user_id', validators=[DataRequired()])
    category_id = StringField('category_id', validators=[DataRequired()])
