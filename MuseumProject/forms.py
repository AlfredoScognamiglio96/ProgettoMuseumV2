from flask_wtf import FlaskForm                                                         #flask_wtf usato per lavorare con i moduli e con i form
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])                  #DataRequired usato per evitare empty form, Email usato per accettare email valide
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    profile_image = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    descrizione = TextAreaField('Content', validators=[DataRequired()])
    profile_post = FileField('Image Post', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Post')