import qrcode
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


def qr_code_generator(absolute_url):
    img = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    img.add_data(absolute_url)
    img.make(fit=True)
    img = img.make_image(fill_color="black", back_color="white").convert('RGB')

    return img


def img_creator(obj):
    if obj.picture and obj.picture.name.split('.')[1] != 'jpg':
        if 'heic' in obj.picture.name.split('.')[1]:
            import pyheif
            picture = obj.picture
            heif_file = pyheif.read_heif(picture)
            picture = Image.frombytes(mode=heif_file.mode, size=heif_file.size, data=heif_file.data)
        else:
            picture = Image.open(obj.picture)

        filename = "%s.jpg" % obj.picture.name.split('.')[0]
        if picture.mode in ('RGBA', 'LA'):
            background = Image.new(picture.mode[:-1], picture.size, '#fff')
            background.paste(picture, picture.split()[-1])
            picture = background
        image_io = BytesIO()
        picture.save(image_io, format='JPEG', quality=100)

        obj.picture.save(filename, ContentFile(image_io.getvalue()), save=False)
        img = Image.open(obj.picture)
        (width, height) = img.size
        if width > 900:
            if 800 / width < 800 / height:
                factor = 800 / height
            else:
                factor = 800 / width

            size = (int(width * factor), int(height * factor))
            img = img.resize(size, Image.ANTIALIAS)
            img.save(obj.picture.path, optimize=True)

    return img
