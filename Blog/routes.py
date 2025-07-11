import os
import secrets
from PIL import Image,ImageOps
from blog import app,db,bcrypt
from flask import render_template,url_for,request,flash,redirect,abort
from blog.form import RegistrationForm,Login,updateuser,New_post,CommentForm
from blog.models import User,Post,Comment
from flask_login import login_user,login_required,logout_user,current_user
from werkzeug.datastructures import FileStorage











