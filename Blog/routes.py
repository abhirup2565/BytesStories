from blog import app,db,bcrypt
from flask import render_template,url_for,request,flash,redirect
from blog.form import RegistrationForm,Login,updateuser,New_post
from blog.models import User,Post
from flask_login import login_user,login_required,logout_user,current_user

@app.route('/')
@app.route('/home')
def home():
    
    return render_template('home.html')

@app.route('/login',methods=("POST","GET"))
def login():
    form = Login()
    if request.method=="POST":
        if form.validate_on_submit():
            email=form.email.data
            user=User.query.filter_by(email=email).first()
            if user and bcrypt.check_password_hash( user.password,form.password.data):
                login_user(user)
                flash("logged in successfully","success")
                return redirect(url_for('home'))
            else:
                flash("username or password incorrect")
    return render_template('login.html',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/signup',methods=("POST","GET"))
def signup():
    form = RegistrationForm()
    if request.method=="POST":
        if form.validate_on_submit() and form.validate():
            user=User()
            user.username=form.username.data
            user.email=form.email.data
            user.password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            db.session.add(user)
            db.session.commit()
            flash("Your account has been created","success")
            return redirect(url_for('login'))
    return render_template('signup.html',form=form)


@app.route('/account',methods=("POST","GET"))
@login_required
def account():
    form=updateuser()
    if request.method=="POST":
        if form.validate_on_submit() and form.validate():
            user=current_user
            user.username=form.username.data
            user.email=form.email.data
            db.session.commit()
            flash("Your account has been updated","success")
            return redirect(url_for('account'))
    elif request.method=="GET":
        if current_user.is_authenticated:
            form.username.data=current_user.username
            form.email.data=current_user.email
    return render_template('account.html',form=form)

@app.route('/new_post',methods=("POST","GET"))
@login_required
def new_post():
    form=New_post()
    if request.method=='POST':
        if form.validate_on_submit():
            post=Post(title=form.title.data,content=form.content.data,user_id=current_user.id)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('new_post.html',form=form)