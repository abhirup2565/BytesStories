def save_content__pic(form_pic,title):
        random_hex = secrets.token_hex(8)
        _,f_ext=os.path.splitext(form_pic.filename)
        picture_fn=random_hex+f_ext
        picture_path=os.path.join(app.root_path,app.config['UPLOAD_CONTENT_FOLDER'],picture_fn)
        
        output_size=(500,500)
        i = Image.open(form_pic)
        fixed_image = ImageOps.exif_transpose(i)
        fixed_image.thumbnail(output_size)
        fixed_image.save(picture_path)
        return picture_fn