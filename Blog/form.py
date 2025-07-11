from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SearchField,EmailField,ValidationError,SubmitField,TextAreaField,FileField
from wtforms.validators import DataRequired,Length,EqualTo
from flask_wtf.file import FileAllowed
from blog.models import User,Post
from flask_login import current_user


            
