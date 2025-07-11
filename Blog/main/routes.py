from flask import Blueprint

main=Blueprint('main',__name__)


@main.route('/')
@main.route('/home')
def home():
    page=request.args.get('page',1,type=int)
    per_page=8
    posts=Post.query.order_by(Post.id.desc()).paginate(page=page,per_page=per_page,error_out=False)
    return render_template('home.html',posts=posts)
