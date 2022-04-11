from datetime import date, datetime, timedelta
from django.core.exceptions import ValidationError


def timer_increase(time_start, fraction):
    time1 = time_start
    time2 = timedelta(minutes=fraction)
    tmp_datetime = datetime.combine(date(1, 1, 1), time1)
    time_end = (tmp_datetime + time2).time()
    return time_end


def validate_date(date):
    if date < datetime.date.today() + datetime.timedelta(days=1):
        raise ValidationError("Data do agendamento deve ser a partir do dia de amanha")
