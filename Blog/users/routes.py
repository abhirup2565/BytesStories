
from blog import db,bcrypt
from flask import render_template,url_for,request,flash,redirect,Blueprint
from blog.users.form import RegistrationForm,Login,updateuser
from blog.users.utility import save_pic
from blog.models import User,Post
from flask_login import login_user,login_required,logout_user,current_user


users=Blueprint('users',__name__)


@users.route('/account',methods=("POST","GET"))
@login_required
def account():
    form=updateuser()
    page=request.args.get('page',1,type=int)
    per_page=4
    my_posts=Post.query.filter_by(author=current_user).paginate(page=page,per_page=per_page,error_out=False)
    if request.method=="POST":
        if form.validate_on_submit():
            if form.profile_pic.data:
                filepath=save_pic(form.profile_pic.data)
                current_user.profile_pic=filepath
            user=current_user
            user.username=form.username.data
            user.email=form.email.data
            db.session.commit()
            flash("Your account has been updated","success")
            return redirect(url_for('users.account'))
    elif request.method=="GET":
        if current_user.is_authenticated:
            form.username.data=current_user.username
            form.email.data=current_user.email   
    return render_template('account.html',form=form,my_posts=my_posts)

@users.route('/login',methods=("POST","GET"))
def login():
    login_form = Login()
    register_form = RegistrationForm()
    if request.method=="POST":
        if "Login" in request.form and login_form.validate_on_submit():
            email=login_form.email.data
            user=User.query.filter_by(email=email).first()
            if user and bcrypt.check_password_hash( user.password,login_form.password.data):
                login_user(user)
                flash("logged in successfully","success")
                return redirect(url_for('main.home'))
            else:
                flash("username or password incorrect")

        elif "Register" in request.form and register_form.validate_on_submit():
            user=User()
            user.username=register_form.username.data
            user.email=register_form.email.data
            user.password=bcrypt.generate_password_hash(register_form.password.data).decode('utf-8')
            user.profile_pic="default.png"
            db.session.add(user)
            db.session.commit()
            flash("Your account has been created","success")
            return redirect(url_for('users.login'))
    return render_template('login_signup.html',login_form=login_form,register_form=register_form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))
