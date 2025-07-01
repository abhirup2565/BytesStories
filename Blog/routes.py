from blog import app,db,bcrypt
from flask import render_template,url_for,request,flash,redirect
from blog.form import RegistrationForm
from blog.models import User

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup',methods=("POST","GET"))
def signup():
    form = RegistrationForm()
    if request.method=="POST":
        if form.validate_on_submit and form.validate():
            user=User()
            user.username=form.username.data
            user.email=form.email.data
            user.password=bcrypt.generate_password_hash(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("Your account has been created","success")
            return redirect(url_for('signup'))
    return render_template('signup.html',form=form)

@app.route('/account')
def account():
    return render_template('account.html')