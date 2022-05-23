import os
import qrcode
import webp
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


def rgb_color_generator(string):
    vowels = "'[] "
    for i in vowels:
        string = string.replace(i, '')
    return string


def qr_code_generator(slug, color=None):
    img = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    img.add_data(str('http://127.0.0.1:8000/' + slug + '/'))
    img.make(fit=True)
    if color and color[1] == "light":
         img = img.make_image(fill_color=color[0], back_color="white").convert('RGB')
    else:
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
    if picture.mode != 'RGB':
        picture = picture.convert('RGB')
    (width, height) = picture.size
    if width > 50:
        if 40 / width < 40 / height:
            factor = 40 / height
        else:
            factor = 40 / width
        size = (int(width * factor), int(height * factor))
        picture = picture.resize(size, Image.ANTIALIAS)

    return picture


def get_logo_rgb(obj):
    rgb = max(obj.getcolors(obj.size[0]*obj.size[1]))
    if (rgb[1][0] * 0.299 + rgb[1][1] * 0.587 + rgb[1][2] * 0.114) > 186:
        rgb_contrast = 'dark'
    else:
        rgb_contrast = 'light'

    rgb = '#%02x%02x%02x' % rgb[1]
    print(rgb_contrast)
    return [rgb, rgb_contrast]


def get_favicon(obj):
    picture = Image.open(obj)
    size = (32, 32)
    picture = picture.resize(size, Image.ANTIALIAS)

    return picture