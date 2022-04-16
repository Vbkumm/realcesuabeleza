from datetime import timedelta, time, datetime, date
from .models import ServiceEquipmentModel


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


def service_equipment_total_time(service, extra_time=None):

    service_equipment_total_time_list = None
    equipment_list = ServiceEquipmentModel.objects.filter(equipment_service=service)

    for equipment_duration in equipment_list:
        if equipment_duration.equipment_replaced is None:
            service_equipment_time = equipment_duration.equipment_time
            if service_equipment_total_time_list is None:
                service_equipment_total_time_list = service_equipment_time
            else:
                service_equipment_total_time_list += service_equipment_time
    if extra_time:
        if extra_time >= 0:
            service_equipment_total_time_list += timedelta(hours=0, minutes=extra_time)
        else:
            if service_equipment_total_time_list > timedelta(hours=0, minutes=extra_time):

                service_equipment_total_time_list -= timedelta(minutes=abs(extra_time),)

    return service_equipment_total_time_list


def service_equipment_description_list(service, hour):
    equipment_list = []
    service_time = time()
    equipment_service_list = ServiceEquipmentModel.objects.filter(equipment_service=service)
    for count, equipment in enumerate(equipment_service_list):
        equipment_name_qtd = equipment.equipment_tittle
        equipment_in_use_time = equipment.equipment_time
        equipment_replaced = equipment.equipment_replaced
        if equipment.equipment_complement:#verifica se equipamento é utilizado ao mesmo tempo q outro ou na sequencia
            if count < 1:#verifica se tempo de uso dos equipamentos substitui ou soma ao tempo do serviço
                equipment_initial_time = hour
                equipment_final_time = timer_increase(equipment_initial_time, total_minutes_int(equipment_in_use_time))
                service_time = equipment_final_time

            else:
                equipment_initial_time = hour
                equipment_final_time = timer_increase(equipment_initial_time, total_minutes_int(equipment_in_use_time))
                if equipment_final_time > service_time:
                    service_time = equipment_final_time
            equipment_list.append([count, equipment_name_qtd.equipment_tittle, equipment_name_qtd.equipment_quantity, equipment_initial_time, equipment_final_time, equipment_replaced, False])

        else:#equipamento não é utilizado ao mesmo tempo / se exitir equipment_replaced ele pode substituir o principal se não o equipamento é utilizado na sequencia
            if equipment.equipment_replaced:
                for equipment_replace in equipment_list:
                    if equipment.equipment_replaced.equipment_tittle == equipment_replace[1]:
                        equipment_replace[2] += equipment_name_qtd.equipment_quantity

            else:

                if count < 1:
                    equipment_initial_time = hour
                    equipment_final_time = timer_increase(equipment_initial_time, total_minutes_int(equipment_in_use_time))
                    service_time = equipment_final_time
                else:
                    equipment_initial_time = service_time
                    equipment_final_time = timer_increase(equipment_initial_time, total_minutes_int(equipment_in_use_time))
                    service_time = equipment_final_time
            equipment_list.append([count, equipment_name_qtd.equipment_tittle, equipment_name_qtd.equipment_quantity, equipment_initial_time, equipment_final_time, equipment_replaced, True])

    return equipment_list
