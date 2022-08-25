from datetime import timedelta, time, datetime, date


def timer_increase(time_start, fraction):
    if fraction:
        time1 = time_start
        time2 = timedelta(minutes=fraction)
        tmp_datetime = datetime.combine(date(1, 1, 1), time1)
        time_end = (tmp_datetime + time2).time()
        return time_end
    else:
        return None


def timer_decrease(time_start, fraction):
    if fraction:
        time1 = time_start
        time2 = fraction
        tmp_datetime = datetime.combine(date(1, 1, 1), time1)
        time_end = (tmp_datetime - time2).time()
        return time_end
    else:
        return None


def time_is_between(timer, timer_range):
    if timer_range[1] and timer_range[0]:
        if timer_range[1] < timer_range[0]:
            return timer >= timer_range[0] or timer < timer_range[1]
        return timer_range[0] <= timer < timer_range[1]
    else:
        return None


def get_hours_min(number):
    minute_text = 'minutos'
    if number == 1:
        minute_text = 'minuto'
    if number >= 60:
        hour = int(number / 60)
        minutes = number - (60 * hour)
        hour_text = 'horas'
        if hour == 1:
            hour_text = 'hora'
        if minutes:
            if minutes == 1:
                minute_text = 'minuto'
            return f'{hour} {hour_text} e {minutes} {minute_text}.'
        return f'{hour} {hour_text}.'
    return f'{number} {minute_text}.'


CHOICES_MIN_TIME = [(i, get_hours_min(i)) for i in range(1, 700)]