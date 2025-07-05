from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SearchField,EmailField,ValidationError,SubmitField,TextAreaField,FileField
from wtforms.validators import DataRequired,Length,EqualTo
from flask_wtf.file import FileAllowed
from blog.models import User,Post
from flask_login import current_user

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
        
class Login(FlaskForm):
    email=EmailField('E-mail',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField("Login")

class updateuser(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=4,max=60)])
    email=EmailField('E-mail',validators=[DataRequired()])
    profile_pic=FileField("Profile Pic",validators=[FileAllowed(['jpg','png','jpeg'])])
    submit=SubmitField("Update")
    
    def validate_username(self,username):
        if username.data!=current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username already taken")
        
    def validate_email(self,email):
        if email.data!=current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("email already taken")
            
class New_post(FlaskForm):
    title = StringField('Title',validators=[DataRequired(),Length(min=4,max=60)])
    content = TextAreaField('Content',validators=[DataRequired(),Length(min=4,max=200)])
    submit=SubmitField("Post")