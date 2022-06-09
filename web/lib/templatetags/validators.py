import os
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import datetime


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.svg', '.gif', '.jpeg', '.jpg', '.png', '.heic', '.webp', '.ico']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Arquivo não suportado! Somente svg, gif, jpeg, png, heic, webp, ico')


def validate_schedule_date(date):
    if date < datetime.date.today() + datetime.timedelta(days=1):
        raise ValidationError("Data do agendamento deve ser a partir do dia de amanha")


FEDERAL_ID_VALIDATE = RegexValidator(
    '(^\d{3}\.\d{3}\.\d{3}\-\d{2}$)|(^\d{2}\.\d{3}\.\d{3}\/\d{4}\-\d{2}$)',
    message="CNPJ ou CPF inválido!"
    )