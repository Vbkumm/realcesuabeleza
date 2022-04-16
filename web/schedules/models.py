from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import datetime, time, timezone
from django.core.exceptions import ValidationError
from professionals.models import ProfessionalModel
from customers.models import CustomerModel
from services.models import ServiceModel, ServiceEquipmentModel
from businesses.models import BusinessAddressModel
from services.utils import service_equipment_total_time, timer_increase, time_is_between
from .utils import validate_schedule_date, fixed_hour


User = get_user_model()


class ScheduleManager(models.Manager):

    def create(self, *args, **kwargs):

        """
        Verifica se horario ja nao esta ocupado por endereco, data, hora, profissional            que vai executar o serviço.
        - self = agendamento a ser consultado
        - schedule_list = lista de agendamentos no dia
        - get_equipments_by_service = lista de equipamentos e tempo de uso por serviço
        """
        available = True

        booking_equipments_extra_time = []
        if self.equipments_extra_time:#lista
            booking_equipments_extra_time = self.schedule_extra_time_set.filter(schedule=self)
        schedule_list = self.__class__.objects.filter(address=self.address, date=self.date,)#lista com agendamentos no dia no endereco do agendamento desejado
        booking_equipment_list = ServiceEquipmentModel.get_service_equipment_time(address=self.address, service=self.service, equipments_extra_time=booking_equipments_extra_time)#retorna tempo total servico e qtd e tempo por equipamento
        booking_end = timer_increase(self.hour, booking_equipment_list[0])
        #verificar agendamentos que utilizam equipamento q e utilizado como substitudo

        for schedule in schedule_list:#agendamento na lista de agendamentos
            if schedule.pk != self.pk:#se nao for o proprio agenadamento
                schedule_equipments_extra_time = []
                if schedule.equipments_extra_time:
                    schedule_equipments_extra_time = schedule.schedule_extra_time_set.filter(schedule=schedule)
                schedule_equipments = ServiceEquipmentModel.get_service_equipment_time(address=schedule.address, service=schedule.service, equipments_extra_time=schedule_equipments_extra_time)#pega equimapentos para realizar o agendamento
                schedule_end = timer_increase(schedule.hour, schedule_equipments[0])

                if time_is_between(fixed_hour(self.hour), (schedule.hour, schedule_end)):#verifica se hora agendada esta entre outros agendamentos
                    if schedule.professional == self.professional:#se tiver outros agendametos na mesma hora do agendamento a ser realizado e e for o mesmo profissional
                        available = False

        if available:
            return super(ScheduleManager, self).create(*args, **kwargs)
        else:
            raise ValidationError("No meio do processo de agendamento tivemos algum problema, parace que "
                                  "este horario ou profissional já não estão mais disponiveis. Tente novamente!")


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

    def equipments_extra_time_list(self):
        if self.equipments_extra_time:
            qs = self.equipments_extra_time

        return self.equipments_extra_time


class ScheduleExtraTimeModel(models.Model):
    """
    Adiciona tempo extra ao agendamento de acordo com o equipamento
    """
    schedule = models.ForeignKey(ScheduleModel, related_name='schedule_extra_time', on_delete=models.CASCADE,)
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
