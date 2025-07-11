import os
from PIL import Image,ImageOps
from flask import current_app
from flask_login import current_user


def save_pic(form_pic):
        name = current_user.username
        _,f_ext=os.path.splitext(form_pic.filename)
        picture_fn=name+f_ext
        picture_path=os.path.join(current_app.root_path,current_app.config['UPLOAD_FOLDER'],picture_fn)
        
        output_size=(450,450)
        i = Image.open(form_pic)
        fixed_image = ImageOps.exif_transpose(i)
        fixed_image.thumbnail(output_size)

        fixed_image.save(picture_path)
        return picture_fn