from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SearchField,EmailField,ValidationError,SubmitField
from wtforms.validators import DataRequired,Length,EqualTo
from blog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=4,max=60)])
    email=EmailField('E-mail',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm_password',validators=[DataRequired(),EqualTo('password',message="Password dont match")])
    submit=SubmitField("Register")

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already exist")
        
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("email already exist")