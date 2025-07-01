from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SearchField,EmailField,ValidationError
from wtforms.validators import DataRequired,Length,EqualTo
from blog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=4,max=60)])
    email=EmailField('E-mail',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm_password',validators=[DataRequired(),EqualTo(password)])