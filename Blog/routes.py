from blog import app
from flask import render_template
from blog.form import RegistrationForm

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    form = RegistrationForm()
    return render_template('signup.html',form=form)

@app.route('/account')
def account():
    return render_template('account.html')