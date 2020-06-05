import os
# pip install pillow OBAVEZNOOO MONI 
from PIL import Image

from flask import url_for, current_app

def add_profile_pic(pic_upload,username):

    filename = pic_upload.filename
    # Uzmi ekstenziju jpg ili png
    ext_type = filename.split('.')[-1]
    storage_filename = str(username) + '.' +ext_type

    filepath = os.path.join(current_app.root_path, 'static\profile_pics', storage_filename)

    # postavljanje velicine fotke eventa.
    output_size = (200, 200)

    # otvori fotku i spremi je
    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)
    pic.save(filepath)

    return storage_filename
