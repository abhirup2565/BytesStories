from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SearchField,EmailField,ValidationError
from wtforms.validators import DataRequired,Length,EqualTo
from blog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('username',validators=[DataRequired(),Length(min=4,max=60)])
    email=EmailField('email',validators=[DataRequired()])
    password=PasswordField('password',validators=[DataRequired()])
    confirm_password=PasswordField('confirm_password',validators=[DataRequired(),EqualTo(password)])