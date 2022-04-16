from datetime import datetime
from django.core.exceptions import ValidationError


def validate_schedule_date(date):
    if date < datetime.date.today() + datetime.timedelta(days=1):
        raise ValidationError("Data do agendamento deve ser a partir do dia de amanha")


def fixed_hour(hour):
    if len(hour.split(':')) > 2:
        hour = datetime.strptime(hour, '%H:%M:%S').time()
    else:
        hour = datetime.strptime(hour, '%H:%M').time()
    return hour
