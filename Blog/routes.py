import os
from PIL import Image,ImageOps
from blog import app,db,bcrypt
from flask import render_template,url_for,request,flash,redirect,abort
from blog.form import RegistrationForm,Login,updateuser,New_post,Comment
from blog.models import User,Post
from flask_login import login_user,login_required,logout_user,current_user
from werkzeug.datastructures import FileStorage


@app.route('/')
@app.route('/home')
def home():
    page=request.args.get('page',1,type=int)
    per_page=8
    posts=Post.query.order_by(Post.id.desc()).paginate(page=page,per_page=per_page,error_out=False)
    return render_template('home.html',posts=posts)

@app.route('/login',methods=("POST","GET"))
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
                return redirect(url_for('home'))
            else:
                flash("username or password incorrect")

        elif "Register" in request.form and login_form.validate_on_submit():
            user=User()
            user.username=register_form.username.data
            user.email=register_form.email.data
            user.password=bcrypt.generate_password_hash(register_form.password.data).decode('utf-8')
            user.profile_pic="default.png"
            db.session.add(user)
            db.session.commit()
            flash("Your account has been created","success")
            return redirect(url_for('login'))
    return render_template('login_signup.html',login_form=login_form,register_form=register_form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))




def save_pic(form_pic):
        name = current_user.username
        _,f_ext=os.path.splitext(form_pic.filename)
        picture_fn=name+f_ext
        picture_path=os.path.join(app.root_path,app.config['UPLOAD_FOLDER'],picture_fn)
        
        output_size=(450,450)
        i = Image.open(form_pic)
        fixed_image = ImageOps.exif_transpose(i)
        fixed_image.thumbnail(output_size)

        fixed_image.save(picture_path)
        return picture_fn


@app.route('/account',methods=("POST","GET"))
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
            return redirect(url_for('account'))
    elif request.method=="GET":
        if current_user.is_authenticated:
            form.username.data=current_user.username
            form.email.data=current_user.email
       
    return render_template('account.html',form=form,my_posts=my_posts)

def save_content__pic(form_pic,title):
        title = title
        _,f_ext=os.path.splitext(form_pic.filename)
        picture_fn=title+f_ext
        picture_path=os.path.join(app.root_path,app.config['UPLOAD_CONTENT_FOLDER'],picture_fn)
        
        output_size=(500,500)
        i = Image.open(form_pic)
        fixed_image = ImageOps.exif_transpose(i)
        fixed_image.thumbnail(output_size)
        fixed_image.save(picture_path)
        return picture_fn

@app.route('/new_post',methods=("POST","GET"))
@login_required
def new_post():
    form=New_post()
    if request.method=='POST':
        if form.validate_on_submit():
            filepath=save_content__pic(form.content_pic.data,form.title.data)
            post=Post(title=form.title.data,content=form.content.data,user_id=current_user.id,content_pic=filepath)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('new_post.html',form=form)

@app.route('/post/<int:post_id>',methods=("POST","GET"))
@login_required
def post(post_id):
    post=Post.query.filter_by(id=post_id).first()
    form=Comment()
    if request.method=="POST":
        if form.validate_on_submit():
            comment=Comment(comment=form.comment.data,user_id=current_user.id,post_id=post.id)
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('post',post_id=post.id,form=form))
    return render_template('post.html',post=post,form=form)

@app.route('/update_post/<int:post_id>',methods=("POST","GET"))
@login_required
def update_post(post_id):
    post=Post.query.filter_by(id=post_id).first()
    if post:
        if current_user!=post.author:
            abort(403)
        form=New_post()
        if request.method=="POST":
            if form.validate_on_submit():
                filepath=save_content__pic(form.content_pic.data,form.title.data)
                post.title=form.title.data
                post.content=form.content.data
                post.content_pic=filepath
                db.session.commit()
                flash("Your post has been updated","success")
                return redirect(url_for('update_post',post_id=post_id))
        elif request.method=="GET":
                form.title.data=post.title
                form.content.data=post.content 
                form.content_pic.data=post.content_pic
    return render_template('update_post.html',form=form,post=post)

@app.route('/delete_post/<int:post_id>')
@login_required
def delete_post(post_id):
    post=Post.query.filter_by(id=post_id).first()
    if post:
        if current_user!=post.author:
            abort(403)
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('home'))
    return redirect(url_for('home'))
