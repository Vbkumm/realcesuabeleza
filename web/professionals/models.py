from django.db import models
from django.db.models import Q, F
from django.db.models.signals import post_save
from realcesuabeleza.settings import CHOICES_WEEKDAY
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from datetime import time, timezone
from django.urls import reverse
from services.utils import CHOICES_MIN_TIME
from .utils import timer_increase, validate_date, _generate_unique_slug
from businesses.models import BusinessModel, BusinessAddressModel
from services.models import ServiceModel, ServiceCategoryModel


User = get_user_model()


class ProfessionalCategoryModel(models.Model):
    """
    Cadastro de categorias de profissionais do salao
    """
    #id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    business = models.ForeignKey(BusinessModel, related_name='business_professional_category', on_delete=models.CASCADE,)
    title = models.CharField('Qual nova categoria de profissional?', max_length=100,)
    slug = models.CharField(unique=True, max_length=150)
    is_active = models.BooleanField(default=True, help_text='Designates whether this professional category should be treated as active. Unselect this instead of deleting professional category.', verbose_name='business category active')
    updated_at = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.SET_NULL, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "professionals_category_list"
        verbose_name = "professionals_category"
        db_table = 'professionals_category_db'
        ordering = ['business',]

    def __str__(self):

        return '%s %s' % (self.pk, self.title)

    def save(self, *args, **kwargs):
        self.slug = _generate_unique_slug(self)
        super(ProfessionalCategoryModel, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('professional_category_detail',  kwargs={"slug": self.business.slug, 'professional_category_slug': self.slug})

    def get_professional_category_by_business(self, business):
        return self.objects.get_queryset(business=business)


class ProfessionalServiceCategoryModel(models.Model):
    """
    Relaciona as categorias de serviços do salão as categorias de profissional que as executam
    """
    professional_category = models.OneToOneField(ProfessionalCategoryModel, related_name='professional_category_set', on_delete=models.CASCADE)
    service_category = models.ManyToManyField(ServiceCategoryModel)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.SET_NULL, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "service_category_professional_category_list"
        verbose_name = "service_category_professional_category"
        db_table = 'service_category_professional_category_db'
        ordering = ['professional_category']


def get_services_by_professional(professional):
    professional_service_list = []
    for professional_category in professional.categories.all():
        service_categories = ProfessionalServiceCategoryModel.objects.filter(professional_category=professional_category).first()
        if service_categories:
            for category in service_categories.service_category.all():
                service_list = ServiceModel.objects.filter(service_category=category, is_active=True)
                professional_service_list += service_list
    # for extra_skill in professional.extra_skills.all():
    #     if extra_skill not in professional_service_list:
    #         professional_service_list.append(extra_skill)
    # for no_skill in professional.no_skills.all():
    #     if no_skill in professional_service_list:
    #         professional_service_list.remove(no_skill)
    return professional_service_list


class ProfessionalQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (Q(name__icontains=query) |
                         Q(title__icontains=query)
                         )

            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs


class ProfessionalManager(models.Manager):

    def get_queryset(self):
        return ProfessionalQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset()


class ProfessionalModel(models.Model):
    """
    Cadastro de profissionais do salao
    """
    business = models.ForeignKey(BusinessModel, related_name='professional_business', on_delete=models.CASCADE,)
    began_date = models.DateField('Qual data de inicio do profissional?', null=True)
    title = models.CharField('Qual o nome do profissional?', max_length=150, null=True)
    federal_id = models.CharField(blank=True, max_length=15, null=True, verbose_name='cpf')
    birth_date = models.CharField('Data de aniversário do profissional*', max_length=150, blank=True, null=True)
    slug = models.CharField(unique=True, max_length=150)
    categories = models.ManyToManyField(ProfessionalCategoryModel, related_name='professional_category', blank=True)
    is_active = models.BooleanField(default=True, help_text='Designates whether this professional should be treated as active. Unselect this instead of deleting professional.', verbose_name='professional business active')
    schedule_active = models.BooleanField('Profissional credenciado ao agendamento online. Marque se sim!', default=False)
    cancel_schedule_active = models.BooleanField('Profissional credenciado a cancelar agendamentos feitos por ele em sua agenda? Marque se sim!', default=False)
    _views = models.PositiveIntegerField(default=0)
    addresses = models.ManyToManyField(BusinessAddressModel, related_name='professional_through_addresses_work', blank=True, through="ProfessionalScheduleModel")
    updated_at = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.SET_NULL, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = ProfessionalManager()

    class Meta:
        verbose_name_plural = "professionals_list"
        verbose_name = "professionals"
        db_table = 'professionals_db'
        ordering = ['business']

    def __str__(self):
        return '%s %s %s' % (self.pk, self.title, self.business)

    def get_absolute_url(self):
        return reverse('professional_detail',  kwargs={"slug": self.business.title, 'professional_slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = _generate_unique_slug(self)

        super(ProfessionalModel, self).save(*args, **kwargs)

    def get_professional_by_business(self, business):
        return self.objects.get_queryset(business=business)

    def professional_grade(self, weekday=None, first_last_time_open_day=None, open_time_list=None, close_time_list=None):
        """
        Monta grade de horarios do profissional
        """
        professional_grade_day = []
        professional_schedule_work_start = None
        professional_schedule_work_end = None
        professional_schedule_time = None
        first_last_time_schedule_day = ProfessionalScheduleModel.objects.first_last_time_schedule_day(weekday)
        if first_last_time_open_day:
            professional_schedule_work_start = first_last_time_open_day[0]
            professional_schedule_work_end = first_last_time_open_day[1]
            professional_schedule_time = first_last_time_open_day[2]
        if first_last_time_schedule_day:
            if first_last_time_open_day:
                if professional_schedule_work_start > first_last_time_schedule_day[0]:
                    professional_schedule_work_start = first_last_time_schedule_day[0]
                if professional_schedule_work_end < first_last_time_schedule_day[1]:
                    professional_schedule_work_end = first_last_time_schedule_day[1]
                if professional_schedule_time < first_last_time_schedule_day[2]:
                    professional_schedule_time = first_last_time_schedule_day[2]
            else:
                professional_schedule_work_start = first_last_time_schedule_day[0]
                professional_schedule_work_end = first_last_time_schedule_day[1]
                professional_schedule_time = first_last_time_schedule_day[2]
        professional_schedule_day = ProfessionalScheduleModel.objects.professional_schedule_day(self, weekday)
        hour = [professional_schedule_work_start, False]
        while hour[0] <= professional_schedule_work_end:
            if professional_schedule_day:
                if professional_schedule_day.professional_schedule_work_start <= hour[0] < professional_schedule_day.professional_schedule_work_end:
                    hour[1] = True
                professional_schedule_time = professional_schedule_day.professional_schedule_time
            if close_time_list:
                for close_time in close_time_list.all():
                    if close_time.close_schedule_initial_hour <= hour[0] < close_time.close_schedule_final_hour:
                        hour[1] = False
            if open_time_list:
                for open_time in open_time_list.all():
                    if open_time.open_schedule_initial_hour <= hour[0] < open_time.open_schedule_final_hour:
                        hour[1] = True
            if hour[0] not in [i[0] for i in professional_grade_day]:
                professional_schedule_hour = hour[0]
                hour[0] = timer_increase(hour[0], professional_schedule_time)
                professional_grade_day.append([professional_schedule_hour, professional_schedule_time, hour[1]])

        return professional_grade_day


def get_professionals_by_business(business=None):
    return ProfessionalModel.objects.filter(business=business, is_active=True)


def get_professional_by_service(service):
    professional_list = []
    professional_category_list = ProfessionalServiceCategoryModel.objects.filter(service_category=service.service_category)
    professionals_in_business = ProfessionalModel.objects.filter(business=service.business, is_active=True)
    for service_professional_category in professional_category_list:
        for professional in professionals_in_business:
            if service in professional.extra_skills.all():
                professional_list.append(professional)
            if service_professional_category.professional_category in professional.categories.all():
                if service not in professional.no_skills.all():
                    professional_list.append(professional)
    return professional_list


class ProfessionalServicesSkillModel(models.Model):

    ''' Controle de habilidades de servicos do profissional '''

    service_skills = models.ManyToManyField(ServiceModel, related_name='professional_service_skill', blank=True,)
    service_no_skills = models.ManyToManyField(ServiceModel, related_name='professional_service_no_skill', blank=True,)
    professional = models.OneToOneField(ProfessionalModel, related_name='service_professional_skill', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "professional_skill_list"
        verbose_name = "professional_skill"
        db_table = 'professional_skill_db'

    @receiver(post_save, sender=ProfessionalModel)
    def get_professional_skill_create(sender, instance, created, **kwargs):
        if created:
            professional_skill = ProfessionalServicesSkillModel.objects.create(professional=instance)
        else:
            professional_skill = ProfessionalServicesSkillModel.objects.get(professional=instance)
        if instance.categories.all():
            for category in instance.categories.all():
                service_category_list = ProfessionalServiceCategoryModel.objects.filter(professional_category=category)
                if service_category_list:
                    for service_category in service_category_list:
                        service_list = ServiceModel.objects.filter(business=instance.business, service_category=service_category)
                        if service_list:
                            for service in service_list:
                                if service not in professional_skill.service_no_skills.all():
                                    if service not in professional_skill.service_skills.all():
                                        professional_skill.service_skills.set(service)
            professional_skill.save()

    @receiver(post_save, sender=ServiceModel)
    def update_service_skill(sender, instance, created, **kwargs):
        if created:
            if instance.service_category:
                professional_category_in_service_category_list = ProfessionalServiceCategoryModel.objects.filter(service_category__in=instance.service_category)
                if professional_category_in_service_category_list:
                    for professional_category_in_service_category in professional_category_in_service_category_list:
                        professional_in_category_list = ProfessionalModel.objects.filter(business=instance.business, categories__in=professional_category_in_service_category)
                        if professional_in_category_list:
                            for professional in professional_in_category_list:
                                professional_skill = ProfessionalServicesSkillModel.objects.filter(professional=professional).first()
                                if professional_skill:
                                    professional_skill.service_skills.set(instance)
                                    professional_skill.save()


class ProfessionalUserModel(models.Model):

    """Correlaciona usuario do app a cadastro de profissional do salão"""

    user = models.ForeignKey(User, related_name='user_professional', on_delete=models.CASCADE)
    professional = models.OneToOneField(ProfessionalModel, related_name='professional_user', on_delete=models.CASCADE)

    updated_at = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='+',on_delete=models.SET_NULL, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['user']


class ProfessionalAddressModel(models.Model):
    """
    Endereço residencial do profissional do salao
    """
    professional = models.ForeignKey(ProfessionalModel, related_name='professional_address', on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True, help_text='Designates whether this address should be treated as active. Unselect this instead of deleting address.', verbose_name='address active')
    zip_code = models.CharField('CEP', max_length=9, null=True, blank=True)
    street = models.CharField('Rua', max_length=100, null=True, blank=True)
    street_number = models.CharField('Numero', max_length=100, null=True, blank=True)
    district = models.CharField('Bairro', max_length=100, null=True, blank=True)
    city = models.CharField('Cidade', max_length=100, null=True, blank=True)
    state = models.CharField('Estado', max_length=100, null=True, blank=True)

    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.SET_NULL, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "professional_address_list"
        verbose_name = "professional_address"
        db_table = 'professional_address_db'
        ordering = ['professional']

    def __str__(self):
        return '%s %s' % (self.professional, self.street)

    def get_address_by_professional(self, professional):
        return self.objects.get_queryset(professional=professional)


class ProfessionalPhoneModel(models.Model):
    professional = models.ForeignKey(ProfessionalModel, related_name='professional_phone', on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField('Telefone', max_length=150, null=True, blank=True)
    is_active = models.BooleanField(default=True, help_text='Designates whether this address should be treated as active. Unselect this instead of deleting address.', verbose_name='phone active')

    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.SET_NULL, blank=True)
    created_by = models.ForeignKey(User, related_name='professional_phone_author', on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "professional_phone_list"
        verbose_name = "professional_phone"
        db_table = 'professional_phone_db'
        ordering = ['professional']

    def __str__(self):
        return '%s %s' % (self.phone, self.professional)

    def get_phone_by_professional(self, professional):
        return self.objects.get_queryset(professional=professional)


class ProfessionalScheduleManager(models.Manager):

    def professional_schedule_day(self, professional, weekday):
        schedule_day = self.get_queryset().filter(professional=professional, week_days=weekday)
        return schedule_day.first()

    def first_last_time_schedule_day(self, weekday):
        first_schedule_day_list = self.get_queryset().filter(week_days=weekday).order_by('start_hour')
        if not first_schedule_day_list:
            first_schedule_day_list = self.get_queryset().all().order_by('start_hour')
        last_schedule_day_list = first_schedule_day_list.order_by('end_hour')
        min_fraction_day = first_schedule_day_list.order_by('fraction_time')
        return first_schedule_day_list.first().professional_schedule_work_start, last_schedule_day_list.last().professional_schedule_work_end, min_fraction_day.first().professional_schedule_time


class ProfessionalScheduleModel(models.Model):
    """
    Cadastro dos dias em que o profissional do salão trabalha no salão
    """

    address = models.ForeignKey(BusinessAddressModel, related_name='professional_address_work', on_delete=models.CASCADE, null=True, blank=True)
    professional = models.ForeignKey(ProfessionalModel, related_name='professional_schedule', on_delete=models.CASCADE)
    week_days = models.IntegerField('Qual dia da semana?', choices=CHOICES_WEEKDAY, default=1)
    start_hour = models.TimeField('Hora da abertura da agenda?', auto_now=False, auto_now_add=False, )
    end_hour = models.TimeField('Ultimo horário da agenda?', auto_now=False, auto_now_add=False, )
    fraction_time = models.IntegerField('Quanto tempo dura cada fração da agenda em minutos?', choices=CHOICES_MIN_TIME, default=40)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.SET_NULL, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = ProfessionalScheduleManager()

    def clean(self, *args, **kwargs):
        if self.end_hour < self.start_hour:
            raise ValidationError("Data inicial deve ser menor que data final assim como hora inicial deve ser menor que hora final.")

        return super().clean()

    class Meta:
        verbose_name_plural = "professional_schedule_list"
        verbose_name = "professional_schedule"
        db_table = 'professional_schedule_db'
        ordering = ['address', 'professional']
        constraints = [
            models.CheckConstraint(
                check=Q(start_hour__lte=F('end_hour')),
                name='schedule_start_before')
        ]

    def __str__(self):
        return '%s %s' % (self.pk, self.week_days)


class OpenScheduleManager(models.Manager):

    def open_date_list(self, business, day_date):
        """
        Primeiro horario aberto no salao
        """
        first_schedule_day_list = self.get_queryset().filter(business=business, start_date__lte=day_date, end_date__gte=day_date).order_by('start_date', 'start_hour')
        if first_schedule_day_list:
            return first_schedule_day_list

    def professional_first_last_time_open_day(self, business, day_date, last_day, professional):
        """
        Primeiro horario aberto profissional do salao com fraçao
        """
        first_schedule_day_list = self.get_queryset().filter(business=business, start_date__gte=day_date, end_date__lte=last_day, professionals__in=[professional] ).order_by('start_hour')
        last_schedule_day_list = first_schedule_day_list.order_by('ending_hour')
        min_fraction_day = first_schedule_day_list.order_by('professionals')
        if first_schedule_day_list:
            return first_schedule_day_list.first().open_schedule_initial_hour, last_schedule_day_list.last().open_schedule_final_hour, min_fraction_day.first().open_professional_schedule_time

    def first_last_time_open_day(self, business, day_date):
        """
        Ultimo horario aberto do salao
        """
        first_schedule_day_list = self.get_queryset().filter(business=business, start_date__lte=day_date, end_date__gte=day_date).order_by('start_hour')
        last_schedule_day_list = first_schedule_day_list.order_by('ending_hour')
        min_fraction_day = first_schedule_day_list.order_by('professionals')
        if first_schedule_day_list:
            return first_schedule_day_list.first().open_schedule_initial_hour, last_schedule_day_list.last().open_schedule_final_hour, min_fraction_day.first().open_professional_schedule_time

    def open_date_valid_professional(self, business, day_date, professional):
        """
        Lista com profissionais do salao com agenda aberta no periodo
        """
        professional_schedule_day_list = self.get_queryset().filter(business=business, start_date__lte=day_date, end_date__gte=day_date, professionals__in=[professional]).order_by('start_hour')
        return professional_schedule_day_list


class OpenScheduleModel(models.Model):
    """
    Abrir agenda do salão por periodo e profissional
    Seleciona data inicial e data final e horarios que quer abrir nesse periodo.
    """

    business = models.ForeignKey(BusinessModel, related_name='open_business', on_delete=models.CASCADE,)
    address = models.ForeignKey(BusinessAddressModel, related_name='open_address_schedule', on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField('Qual data inicial para abrir a agenda?', auto_now=False, auto_now_add=False, validators=[validate_date],)
    end_date = models.DateField('Qual data final para abrir a agenda?', auto_now=False, auto_now_add=False, validators=[validate_date],)
    start_hour = models.TimeField('Qual horário inicial para abrir a agenda?', auto_now=False, auto_now_add=False, default=time(00, 00))
    end_hour = models.TimeField('Qual horário final para abrir a agenda?', auto_now=False, auto_now_add=False, default=time(00, 00))
    fraction_time = models.IntegerField('Quanto tempo dura cada fração da agenda em minutos?', choices=CHOICES_MIN_TIME, default=40)
    professionals = models.ManyToManyField(ProfessionalModel, related_name='open_professionals', blank=True)
    description = models.CharField('Observações:', max_length=1000, null=True, blank=True)

    updated_at = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.SET_NULL, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = OpenScheduleManager()

    def clean(self, *args, **kwargs):
        if self.end_date < self.start_date or self.end_hour < self.start_hour:
            raise ValidationError("Data inicial deve ser menor que data final assim como hora inicial deve ser menor que hora final.")

        return super().clean()

    class Meta:
        verbose_name_plural = "open_schedule_list"
        verbose_name = "open_schedule"
        db_table = 'open_schedule_db'
        ordering = ["business", "address"]
        constraints = [
            models.CheckConstraint(
                check=Q(start_date__lte=F('end_date'), start_hour__lte=F('end_hour')),
                name='open_start_before')
        ]

    def future_open_schedule_professional(self, professional):
        """
        Filtra abertura de agendanda no futuro por profissional
        """
        return self.objects.get_queryset(professionals__in=professional, end_date__gte=timezone.now()).order_by('start_date')

    def passed_open_schedule_professional(self, professional):
        """
        Filtra abertura de agendanda no passado por profissional
        """
        return self.objects.get_queryset(professionals__in=professional, end_date__lt=timezone.now())


class CloseScheduleManager(models.Manager):

    def close_date_list(self, business, day_date):
        first_schedule_day_list = self.get_queryset().filter(business=business, start_date__lte=day_date, end_date__gte=day_date).order_by('start_date', 'start_hour')
        if first_schedule_day_list:
            return first_schedule_day_list

    def close_date_valid_professional(self, business, day_date, professional):
        professional_schedule_day_list = self.get_queryset().filter(business=business, start_date__lte=day_date, end_date__gte=day_date, professionals__in=[professional]).order_by('start_hour')
        return professional_schedule_day_list


class CloseScheduleModel(models.Model):
    """
    Fechar agenda do salao por periodo e profissional
    Seleciona data inicial e data final e horarios que quer fechar nesse periodo.
    """
    business = models.ForeignKey(BusinessModel, related_name='close_business', on_delete=models.CASCADE,)
    address = models.ForeignKey(BusinessAddressModel, related_name='close_address_schedule', on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField('Qual data inicial para fechar a agenda?', auto_now=False, auto_now_add=False, validators=[validate_date],)
    end_date = models.DateField('Qual data final para fechar a agenda?', auto_now=False, auto_now_add=False, validators=[validate_date],)
    start_hour = models.TimeField('Qual horário inicial para fechar a agenda?', auto_now=False, auto_now_add=False, default=time(00, 00))
    end_hour = models.TimeField('Qual horário final para fechar a agenda?', auto_now=False, auto_now_add=False, default=time(00, 00))
    professionals = models.ManyToManyField(ProfessionalModel, related_name='close_professionals', blank=True)
    description = models.CharField('Observações:', max_length=1000, null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.SET_NULL, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = CloseScheduleManager()

    def clean(self, *args, **kwargs):
        if self.end_date < self.start_date or self.end_hour < self.start_hour:
            raise ValidationError("Data inicial deve ser menor que data final assim como hora inicial deve ser menor que hora final.")

        return super().clean()

    class Meta:
        verbose_name_plural = "close_schedule_list"
        verbose_name = "close_schedule"
        db_table = 'close_schedule_db'
        ordering = ["business", "address"]
        constraints = [
            models.CheckConstraint(
                check=Q(start_date__lte=F('end_date'), start_hour__lte=F('end_hour')),
                name='close_start_before')
        ]

    def future_close_schedule_professional(self, professional):
        """
        Filtra fechamento de agendanda no futuro por profissional
        """
        return self.objects.get_queryset(professionals__in=professional, end_date__gte=timezone.now()).order_by('start_date')

    def passed_close_schedule_professional(self, professional):
        """
        Filtra fechamento de agendanda no passado por profissional
        """
        return self.objects.get_queryset(professionals__in=professional, end_date__lt=timezone.now())
