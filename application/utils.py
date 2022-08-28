import os
import secrets
from PIL import Image
from application import app

def currencyconvert(rupee):

    if (rupee.is_integer()):
        rupee = round(rupee)
    
    return "₹"+ str(rupee)




def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/product_img', picture_fn)
    output_size = (300, 300)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn
