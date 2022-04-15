from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import datetime, time, timezone
from professionals.models import ProfessionalModel
from customers.models import CustomerModel
from services.models import ServiceModel, ServiceEquipmentModel
from businesses.models import BusinessAddressModel
from services.utils import service_equipment_total_time, timer_increase, time_is_between
from .utils import validate_schedule_date, fixed_hour


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
    equipments_extra_time = models.ManyToManyField(ServiceEquipmentModel, blank=True, through="ScheduleExtraTimeModel")

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

    def schedule_by_address_by_date(self, address):
        """
        Filtra agendamentos por endereço do salao
        """
        upcoming = self.objects.get_queryset(date__gte=timezone.now(), address=address).order_by('date')
        passed = self.objects.get_queryset(date__lt=timezone.now(), address=address).order_by('date')
        return [upcoming, passed]

    def schedule_by_professional_by_date(self, professional):
        """
       Filtra agendamentos por profissional do salao
       """
        upcoming = self.objects.get_queryset(date__gte=timezone.now(), professional=professional).order_by('date')
        passed = self.objects.get_queryset(date__lt=timezone.now(), address=professional).order_by('date')
        return [upcoming, passed]

    def schedule_by_customer_by_date(self, customer):
        """
       Filtra agendamentos por cliente do salao
       """
        upcoming = self.objects.get_queryset(date__gte=timezone.now(), customer=customer).order_by('date')
        passed = self.objects.get_queryset(date__lt=timezone.now(), address=customer).order_by('date')
        return [upcoming, passed]

    def schedule_check_is_future(self):
        date_hour = ('%s %s' % (self.date, self.hour))
        date_hour = datetime.strptime(date_hour, '%Y-%m-%d %H:%M:%S')
        if datetime.today() < date_hour:
            return True

    def schedule_is_available(self):
        """
        Verifica se horario ja nao esta ocupado por endereco, data, hora, profissional
        que vai executar o serviço.
        - self = agendamento a ser consultado
        - schedule_list = lista de agendamentos no dia
        - get_equipments_by_service = lista de equipamentos e tempo de uso por serviço

        """
        available = True
        schedule_list = self.__class__.objects.filter(address=self.address, date=self.date,)#lista com agendamentos no dia
        booking_equipments = ServiceEquipmentModel.objects.get(service=self.service)#pega equimapentos para realizar o agendamento
        booking_equipments_extra_time = self.equipments_extra_time#lista

        for schedule in schedule_list:#agendamento na lista de agendamentos
            if schedule.pk != self.pk:#se nao for o proprio agenadamento
                schedule_equipments = ServiceEquipmentModel.objects.get(service=schedule.service)#pega equimapentos para realizar o agendamento
                schedule_equipments_extra_time = schedule.equipments_extra_time

                schedule_total_time = schedule.extra_time       #lista com equipamentos do servico e tempo extra em cada um
                schedule_equipment_obj_list = []
                for equipment in schedule_equipments:# equipamentos do agendamento

                    if ServiceEquipmentModel.get_equipment_time(equipment):
                        equipment_time = ServiceEquipmentModel.get_equipment_time(equipment)#retorna inteiro = tempo de uso do equipamento em minutos
                        schedule_equipment_obj_list.append()
                        schedule_total_time += equipment_time
                schedule_end = timer_increase(schedule.hour, schedule_total_time)

                if time_is_between(fixed_hour(self.hour), (schedule.hour, schedule_end)):#verifica se hora agendada esta entre outros agendamentos
                    if schedule.professional == self.professional:#se tiver outros agendametos na mesma hora do agendamento a ser realizado e e for o mesmo profissional
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


class ScheduleExtraTimeModel(models.Model):
    """
    Adiciona tempo extra ao agendamento de acordo com o equipamento
    """
    schedule = models.ForeignKey(ScheduleModel, on_delete=models.CASCADE,)
    service_equipment = models.ForeignKey(ServiceEquipmentModel, on_delete=models.CASCADE)
    extra_time = models.IntegerField('Se necessario corrija o tempo de execução do serviço de acordo com a cliente:', default=0)

    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.SET_NULL, blank=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "schedule_extra_time_list"
        verbose_name = "schedule_extra_time"
        db_table = 'schedule_extra_time_db'
