from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    profile_image = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    descrizione = TextAreaField('Content', validators=[DataRequired()])
    immagine = FileField('Image Post', validators=[FileAllowed(['jpg','png'])])             #NEW LINE ADD
    submit = SubmitField('Post')