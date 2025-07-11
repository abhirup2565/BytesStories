
class New_post(FlaskForm):
    title = StringField('Title',validators=[DataRequired(),Length(min=4,max=120)])
    content = TextAreaField('Content',validators=[DataRequired(),Length(min=4,max=1200)])
    content_pic=FileField("Content Pic",validators=[FileAllowed(['jpg','png','jpeg'])])
    submit=SubmitField("Post")

class CommentForm(FlaskForm):
    comment = TextAreaField('comment',validators=[DataRequired(),Length(min=4,max=600)])
    submit=SubmitField("Comment")