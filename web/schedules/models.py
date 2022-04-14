from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import datetime, time, timezone
from professionals.models import ProfessionalModel
from customers.models import CustomerModel
from services.models import ServiceModel, ServiceEquipmentModel
from businesses.models import BusinessAddressModel
from services.utils import service_equipment_total_time, timer_increase, total_minutes_int, time_is_between
from .utils import validate_schedule_date


User = get_user_model()


class ScheduleManager(models.Manager):

    pass


class ScheduleModel(models.Model):

    address = models.ForeignKey(BusinessAddressModel, related_name='schedule_business_address', on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(ServiceModel, related_name='schedule_service', on_delete=models.SET_NULL, blank=True, null=True)
    customer = models.ForeignKey(CustomerModel, related_name='schedule_customer', on_delete=models.SET_NULL, blank=True, null=True)
    professional = models.ForeignKey(ProfessionalModel, related_name='schedule_professional', on_delete=models.SET_NULL, blank=True, null=True)

    date = models.DateField('Qual dia você deseja agendar?', auto_now=False, auto_now_add=False, validators=[validate_schedule_date],)
    hour = models.TimeField('Qual horário você deseja agendar?', auto_now=False, auto_now_add=False, default=time(00, 00))
    description = models.CharField('Observações:', max_length=1000, null=True, blank=True)

    _done = models.BooleanField('Escolha a opção?', default=False)
    _paid = models.BooleanField('Seviço pago?', default=False)
    _canceled = models.BooleanField('Seviço cancelado?', default=False)
    extra_time = models.IntegerField('Se necessario corrija o tempo de execução do serviço de acordo com a cliente:', default=0)

    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.SET_NULL, blank=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = ScheduleManager()

    class Meta:
        verbose_name_plural = "schedule_list"
        verbose_name = "schedules"
        db_table = 'schedules_db'
        #constraints = [models.UniqueConstraint(fields=['schedule_date', 'schedule_hour', 'schedule_professional', ], name='unique_schedule')]

    def __str__(self):
        return '%s %s %s %s' % (self.pk, self.customer, self.professional, self.address)

    def get_absolute_url(self):
        return reverse('schedules:detail', kwargs={'pk': self.pk})

    def schedule_check_is_future(self):
        time_now = datetime.today()
        hour = ('%s %s' % (self.date, self.hour))
        hour = datetime.strptime(hour, '%Y-%m-%d %H:%M:%S')
        if time_now < hour:
            return True

    def schedule_by_date(self):
        pass

    def schedule_is_available(self):
        available = True
        schedule_list = self.__class__.objects.filter(date=self.date)
        schedule_hour = self.hour
        if len(schedule_hour.split(':')) > 2:
            schedule_hour = datetime.strptime(schedule_hour, '%H:%M:%S').time()
        else:
            schedule_hour = datetime.strptime(schedule_hour, '%H:%M').time()
        for schedule in schedule_list:
            equipment_time_booked = service_equipment_total_time(schedule.service, schedule.extra_time)
            schedule_end = timer_increase(schedule.hour, total_minutes_int(equipment_time_booked))
            if time_is_between(schedule_hour, (schedule.hour, schedule_end)):
                if schedule.professional == self.professional:
                    if schedule.pk != self.pk:
                        available = False

        return available

    def busy_equipment_in_service_schedule_hour(self):
        service = self.service
        equipment_service_list = ServiceEquipmentModel.objects.filter(service=service)
        service_time = time()
        equipment_list = []
        for count, equipment_service in enumerate(equipment_service_list):
            equipment = service.tittle
            equipment_name = equipment.equipment_tittle
            equipment_in_use_time = equipment_service.equipment_time
            equipment_qtd = equipment.equipment_quantity
            equipment_replaced = equipment_service.equipment_replaced
            if equipment_service.equipment_complement:#verifica se equipamento é utilizado ao mesmo tempo q outro ou na sequencia
                if count < 1:#verifica se tempo de uso dos equipamentos substitui ou soma ao tempo do serviço
                    equipment_initial_time = self.hour
                    equipment_final_time = timer_increase(equipment_initial_time, total_minutes_int(equipment_in_use_time))
                    service_time = equipment_final_time

                else:
                    equipment_initial_time = self.hour
                    equipment_final_time = timer_increase(equipment_initial_time, total_minutes_int(equipment_in_use_time))
                    if equipment_final_time > service_time:
                        service_time = equipment_final_time
                equipment_list.append([count, equipment_name, equipment_qtd, equipment_initial_time, equipment_final_time, equipment_replaced, False])

            else:#equipamento não é utilizado ao mesmo tempo / se exitir equipment_replaced ele pode substituir o principal se não o equipamento é utilizado na sequencia
                if count < 1:
                    equipment_initial_time = self.hour
                    equipment_final_time = timer_increase(equipment_initial_time, total_minutes_int(equipment_in_use_time))
                    service_time = equipment_final_time
                else:
                    equipment_initial_time = service_time
                    equipment_final_time = timer_increase(equipment_initial_time, total_minutes_int(equipment_in_use_time))
                    service_time = equipment_final_time
                equipment_list.append([count, equipment_name, equipment_qtd, equipment_initial_time, equipment_final_time, equipment_replaced, True])
        return equipment_list

