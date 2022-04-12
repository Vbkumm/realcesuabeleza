from datetime import date, datetime, timedelta
from django.core.exceptions import ValidationError


def timer_increase(time_start, fraction):
    """
    Adiciona minutos a hora marcada
    """
    time1 = time_start
    time2 = timedelta(minutes=fraction)
    tmp_datetime = datetime.combine(date(1, 1, 1), time1)
    time_end = (tmp_datetime + time2).time()
    return time_end


def validate_date(date_):
    """
    Verifica se data do agendamento é igual ou maior que hoje
    """
    if date_ < date.today():
        raise ValidationError("Data do agendamento deve ser igual ou maior que o dia de hoje!")

