
from blog import db
from flask import render_template,url_for,request,flash,redirect,abort,Blueprint
from blog.posts.form import New_post,CommentForm
from blog.posts.utility import save_content__pic
from blog.models import Post,Comment
from flask_login import login_required,current_user


posts=Blueprint('posts',__name__)

@posts.route('/new_post',methods=("POST","GET"))
@login_required
def new_post():
    form=New_post()
    if request.method=='POST':
        if form.validate_on_submit():
            post=Post(title=form.title.data,content=form.content.data,user_id=current_user.id)
            if form.content_pic.data:
                filepath=save_content__pic(form.content_pic.data,form.title.data)
                post.content_pic=filepath
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('main.home'))
    return render_template('new_post.html',form=form)

@posts.route('/post/<int:post_id>',methods=("POST","GET"))
@login_required
def post(post_id):
    post=Post.query.filter_by(id=post_id).first()
    DisplayComments=Comment.query.filter_by(post_id=post_id).all()
    form=CommentForm()
    if request.method=="POST":
        if form.validate_on_submit():
            comment=Comment(comment=form.comment.data,user_id=current_user.id,post_id=post.id)
            db.session.add(comment)
            db.session.commit()
            flash("Comment successfully posted","success")
            return redirect(url_for('posts.post',DisplayComments=DisplayComments,post_id=post.id,form=form))
        else:
           flash("There was an error","info") 
    return render_template('post.html',DisplayComments=DisplayComments,post=post,form=form)

@posts.route('/update_post/<int:post_id>',methods=("POST","GET"))
@login_required
def update_post(post_id):
    post=Post.query.filter_by(id=post_id).first()
    if post:
        if current_user!=post.author:
            abort(403)
        form=New_post()
        if request.method=="POST":
            if form.validate_on_submit():
                if form.content_pic.data:
                    filepath=save_content__pic(form.content_pic.data,form.title.data)
                    post.content_pic= filepath
                post.title=form.title.data
                post.content=form.content.data
                db.session.commit()
                flash("Your post has been updated","success")
                return redirect(url_for('posts.update_post',post_id=post_id))
        elif request.method=="GET":
                form.title.data=post.title
                form.content.data=post.content 
                form.content_pic.data=post.content_pic
    return render_template('update_post.html',form=form,post=post)

@posts.route('/delete_post/<int:post_id>')
@login_required
def delete_post(post_id):
    post=Post.query.filter_by(id=post_id).first()
    if post:
        if current_user!=post.author:
            abort(403)
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('main.home'))
    return redirect(url_for('main.home'))