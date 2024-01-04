from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired


class RequiredIfUpdate(DataRequired):
    def __call__(self, form, field):
        if getattr(form, 'is_update', False):
            super(RequiredIfUpdate, self).__call__(form, field)


class PostForm(FlaskForm):
    id = StringField('ID', validators=[RequiredIfUpdate(message='ID is required on update.')])
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    user_id = StringField('user_id', validators=[DataRequired()])
    category_id = StringField('category_id', validators=[DataRequired()])
