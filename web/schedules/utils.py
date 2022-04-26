from datetime import datetime, date, timedelta
from django.core.exceptions import ValidationError


def validate_schedule_date(user_date):
    """
    Verifica se a data do agendamento é maior que a data do dia
    """
    if user_date < date.today() + timedelta(days=0):
        raise ValidationError("Data do agendamento deve ser a partir do dia de amanha")


def fixed_hour(hour):
    if len(hour.split(':')) > 2:
        hour = datetime.strptime(hour, '%H:%M:%S').time()
    else:
        hour = datetime.strptime(hour, '%H:%M').time()
    return hour
