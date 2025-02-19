from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from kim_gallery import db

class UploadForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    image = FileField('Image or Video', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'mp4'], 'Images and MP4 videos only!')
    ])
    tags = StringField('Tags (comma separated)', validators=[Length(max=200)])
    submit = SubmitField('Upload')

class EditImageForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    tags = StringField('Tags (comma separated)', validators=[Length(max=200)])
    submit = SubmitField('Save Changes') 