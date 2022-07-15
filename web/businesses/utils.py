import os
import qrcode
import webp
from PIL import Image
from collections import defaultdict
from realcesuabeleza.settings import WEEKDAYS_CHOICES
from io import BytesIO
from django.core.files.base import ContentFile


def rgb_color_generator(string):
    vowels = "'[] "
    if string:
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


def make_work_hour_schedule(business_address_days_hour_list):
    new_day_hours_list = []
    if business_address_days_hour_list:
        address_hours_days = []
        for hours_days in business_address_days_hour_list:
            if hours_days.is_active:
                for day in WEEKDAYS_CHOICES:
                    if str(hours_days.week_days) == day[0]:
                        address_hours_days.append({'week_days': day[1], 'start_hour': hours_days.start_hour, 'end_hour': hours_days.end_hour,})
                        #transforma queryset em lista com dados necessarios
        tmp = defaultdict(list)
        for item in address_hours_days:
            tmp[item['week_days']].append([item['start_hour'], item['end_hour']])
        parsed_list = [{'week_days': k, 'hours': v} for k, v in tmp.items()]#une dias iguais e forma lista de horas no dia
        for days in parsed_list:#tira horarios repetidos
            new_hour_list = []
            for hours in days['hours']:
                if new_hour_list:
                    for new_hour in new_hour_list:
                        if new_hour[0] >= hours[0] and new_hour[1] < hours[1]:
                            new_hour_list.remove(new_hour)
                            new_hour_list.append([hours[0], hours[1]])
                        if hours[1] > new_hour[1] >= hours[0]:
                            new_hour[1] = hours[1]
                        if hours[0] > new_hour[1] < hours[1]:
                            new_hour_list.append([hours[0], hours[1]])
                else:
                    new_hour_list.append([hours[0], hours[1]])
            new_day_hours_list.append({'week_days': days['week_days'], 'hours': new_hour_list})
    return new_day_hours_list
