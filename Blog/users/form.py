

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=4,max=60)])
    email=EmailField('E-mail',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm_password',validators=[DataRequired(),EqualTo('password',message="Password dont match")])
    submit=SubmitField(label="Register",name="Register")

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
    submit=SubmitField(label="Login",name="Login")
    
    def validate_email(self,email):
            user = User.query.filter_by(email=email.data).first()
            if not user:
                raise ValidationError("No account registered with this email")

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