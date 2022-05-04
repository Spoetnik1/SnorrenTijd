from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField, StringField


class PictureSubmitForm(FlaskForm):
    picture = FileField('Upload file for mustache addition', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Upload File!')