import os
import qrcode
import webp
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


def qr_code_generator(slug):
    img = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    img.add_data(str('http://127.0.0.1:8000/' + slug + '/'))
    img.make(fit=True)
    img = img.make_image(fill_color="black", back_color="white").convert('RGB')

    return img


def get_logo_img(obj):

    if 'heic' in obj.name.split('.')[1]:
        import pyheif
        picture = obj
        heif_file = pyheif.read_heif(picture)
        picture = Image.frombytes(mode=heif_file.mode, size=heif_file.size, data=heif_file.data)
    else:
        picture = Image.open(obj)
    if picture.mode in ('RGBA', 'LA'):
        picture.convert('RGB')
    (width, height) = picture.size
    if width > 50:
        if 40 / width < 40 / height:
            factor = 40 / height
        else:
            factor = 40 / width
        size = (int(width * factor), int(height * factor))
        picture = picture.resize(size, Image.ANTIALIAS)

    return picture


def get_favicon(obj):
    picture = Image.open(obj)
    (width, height) = picture.size
    if width > 5:
        if 4 / width < 4 / height:
            factor = 4 / height
        else:
            factor = 4 / width
        size = (int(width * factor), int(height * factor))
        picture = picture.resize(size, Image.ANTIALIAS)

    return picture