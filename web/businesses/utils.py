import os
import json
import qrcode
from datetime import datetime, time
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


def is_time_now(start_hour, end_hour, weekday):
    if start_hour <= datetime.now().time() <= end_hour and weekday == datetime.now().weekday():
        return True
    return False


def make_hours_day(hour_list, weekday):
    new_hour_list = []
    is_now = {'is_now': False, 'week_day': None}
    is_today = False
    for hours in hour_list:
        if is_time_now(hours[0], hours[1], weekday):
            is_now = {'is_now': True, 'week_day': weekday}
        if new_hour_list:
            for new_hour in new_hour_list:
                if datetime.strptime(new_hour[0], "%H:%M").time() >= hours[0] and datetime.strptime(new_hour[1], "%H:%M").time() < hours[1]:
                    new_hour_list.remove(new_hour)
                    new_hour_list.append([hours[0].strftime("%H:%M"), hours[1].strftime("%H:%M")])
                if hours[1] > datetime.strptime(new_hour[1], "%H:%M").time() >= hours[0]:
                    new_hour[1] = hours[1].strftime("%H:%M")
                if hours[0] > datetime.strptime(new_hour[1], "%H:%M").time() < hours[1]:
                    new_hour_list.append([hours[0].strftime("%H:%M"), hours[1].strftime("%H:%M")])
        else:
            new_hour_list.append([hours[0].strftime("%H:%M"), hours[1].strftime("%H:%M")])
        if is_now:
            is_today = is_now
    return [new_hour_list, is_today]


def make_work_hour_schedule(business_address_days_hour_list, address_pk):
    new_day_hours_list = []
    is_now = False
    if business_address_days_hour_list:
        tmp = defaultdict(list)

        for item in list(business_address_days_hour_list.values('week_days', 'start_hour', 'end_hour')):
            tmp[item['week_days']].append([item['start_hour'], item['end_hour']])
        parsed_list = [{'week_days': k, 'hours': v} for k, v in tmp.items()]#une dias iguais e forma lista de horas no dia
        for days in parsed_list:#tira horarios repetidos

            #tirar horas repetidas ou sobrepostas
            new_hour_list = make_hours_day(days['hours'], days['week_days'])

            for week_day in WEEKDAYS_CHOICES:#muda dia em numero para o dia da semana
                if str(days['week_days']) == week_day[0]:
                    print(f"week_days {days['week_days']} --{new_hour_list[1]} ---")
                    if new_hour_list[1]['week_day'] is not None:
                        if days['week_days'] == new_hour_list[1]['week_day'] and new_hour_list[1] and days['week_days'] == datetime.now().weekday():
                            is_now = True
                    new_day_hours_list.append({'week_days': week_day[1], 'is_now': is_now, 'hours': new_hour_list[0],})
    return [json.dumps(new_day_hours_list), is_now, json.dumps(address_pk)]
