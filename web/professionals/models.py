from django.db import models
from django.db.models import Q, F
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from datetime import time
from django.urls import reverse
from django.utils.text import slugify
from .utils import timer_increase, validate_date, _generate_unique_slug
from businesses.models import BusinessModel
from services.models import ServiceModel, ServiceCategoryModel


User = get_user_model()


class ProfessionalCategoryModel(models.Model):
    """
    Cadastro de categorias de profissionais do salao
    """
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    business = models.ForeignKey(BusinessModel, related_name='business_professional_category', on_delete=models.CASCADE,)
    title = models.CharField('Qual nova categoria de profissional?', max_length=100,)
    slug = models.CharField(unique=True, max_length=150)
    service_category = models.ManyToManyField(ServiceCategoryModel, blank=True, through="ProfessionalServiceCategoryModel")
    is_active = models.BooleanField(default=True, help_text='Designates whether this professional category should be treated as active. Unselect this instead of deleting professional category.', verbose_name='business category active')
    updated_at = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.SET_NULL, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "professionals_category_list"

    def __str__(self):

        return '%s %s' % (self.pk, self.title)

    def save(self, *args, **kwargs):
        self.slug = _generate_unique_slug(self)
        super(ProfessionalCategoryModel, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('professionals:category',  kwargs={"slug": self.slug})


class ProfessionalServiceCategoryModel(models.Model):
    """
    Relaciona as categorias de serviços do salão as categorias de profissional que as executam
    """
    service_category = models.ForeignKey(ServiceCategoryModel, on_delete=models.CASCADE)
    professional_category = models.ForeignKey(ProfessionalCategoryModel, on_delete=models.CASCADE, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)


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
    name = models.CharField('Qual o nome do profissional?', max_length=150, null=True)
    federal_id = models.CharField(blank=True, max_length=15, null=True, unique=True, verbose_name='cnpj')
    birth_date = models.CharField('Data de aniversário do profissional*', max_length=150, blank=True, null=True)
    slug = models.CharField(unique=True, max_length=150)
    category = models.ManyToManyField(ProfessionalCategoryModel, related_name='professional_category', blank=True)
    is_active = models.BooleanField(default=True, help_text='Designates whether this professional should be treated as active. Unselect this instead of deleting professional.', verbose_name='professional business active')
    schedule_active = models.BooleanField('Profissional credenciado ao agendamento online. Marque se sim!', default=False)
    cancel_schedule_active = models.BooleanField('Profissional credenciado a cancelar agendamentos feitos por ele em sua agenda? Marque se sim!', default=False)
    _views = models.PositiveIntegerField(default=0)
    extra_skills = models.ManyToManyField(ServiceModel, related_name='extra_skill', blank=True, through="ProfessionalExtraSkillModel")
    no_skills = models.ManyToManyField(ServiceModel, related_name='no_skill', blank=True, through="ProfessionalNoSkillModel")
    updated_at = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.SET_NULL, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = ProfessionalManager()

    class Meta:
        verbose_name_plural = "professionals_list"
        verbose_name = "professionals"
        db_table = 'professionals_db'

    def __str__(self):
        return '%s %s %s' % (self.pk, self.name, self.business)

    def get_absolute_url(self):
        return reverse('professionals:detail',  kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.slug).lower()

        super(ProfessionalModel, self).save(*args, **kwargs)

    def professional_grade(self, weekday, first_last_time_open_day=None, open_time_list=None, close_time_list=None):
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


class ProfessionalExtraSkillModel(models.Model):
    """
    Relaciona serviços do salão o qual não fazem parte da categoria de profissional mas o profissional executa
    """
    service = models.ForeignKey(ServiceModel, on_delete=models.CASCADE)
    professional = models.ForeignKey(ProfessionalModel, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)


class ProfessionalNoSkillModel(models.Model):
    """
    Relaciona serviços do salão o qual fazem parte da categoria de profissional mas o profissional não executa
    """
    service = models.ForeignKey(ServiceModel, on_delete=models.CASCADE)
    professional = models.ForeignKey(ProfessionalModel, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)


class ProfessionalUserModel(models.Model):

    """Correlaciona usuario do app a cadastro de profissional do salão"""

    user = models.ForeignKey(User, related_name='user_professional', on_delete=models.CASCADE)
    professional = models.OneToOneField(ProfessionalModel, related_name='professional_user', on_delete=models.CASCADE)

    updated_at = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='+',on_delete=models.SET_NULL, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)


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
    created_by = models.ForeignKey(User, related_name='professional_address_author', on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "professional_address_list"
        verbose_name = "professional_address"
        db_table = 'professional_address_db'

        def __str__(self):
            return '%s %s' % (self.professional, self.street)


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

        def __str__(self):
            return '%s %s' % (self.phone, self.professional)


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
    CHOICES_WEEKDAY = [(i, i) for i in range(0, 7)]
    CHOICES_MIN_TIME = [(i, i) for i in range(1, 300)]

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
    CHOICES_MIN_TIME = [(i, i) for i in range(1, 300)]

    business = models.ForeignKey(BusinessModel, related_name='open_business', on_delete=models.CASCADE,)
    start_date = models.DateField('Qual data inicial para abrir a agenda?', auto_now=False, auto_now_add=False, validators=[validate_date],)
    end_date = models.DateField('Qual data final para abrir a agenda?', auto_now=False, auto_now_add=False, validators=[validate_date],)
    start_hour = models.TimeField('Qual horário inicial para abrir a agenda?', auto_now=False, auto_now_add=False, default=time(00, 00))
    end_hour = models.TimeField('Qual horário final para abrir a agenda?', auto_now=False, auto_now_add=False, default=time(00, 00))
    fraction_time = models.IntegerField('Quanto tempo dura cada fração da agenda em minutos?', choices=CHOICES_MIN_TIME, default=40)
    professionals = models.ManyToManyField(ProfessionalModel, related_name='open_professionals', blank=True)
    description = models.CharField('Observações:', max_length=1000, null=True, blank=True)

    updated_at = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.SET_NULL, blank=True)
    created_by = models.ForeignKey(User, related_name='open_schedule_user', on_delete=models.SET_NULL, blank=True, null=True)
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
        ordering = ["business"]
        constraints = [
            models.CheckConstraint(
                check=Q(start_date__lte=F('end_date'), start_hour__lte=F('end_hour')),
                name='open_start_before')
        ]


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
    start_date = models.DateField('Qual data inicial para fechar a agenda?', auto_now=False, auto_now_add=False, validators=[validate_date],)
    end_date = models.DateField('Qual data final para fechar a agenda?', auto_now=False, auto_now_add=False, validators=[validate_date],)
    start_hour = models.TimeField('Qual horário inicial para fechar a agenda?', auto_now=False, auto_now_add=False, default=time(00, 00))
    end_hour = models.TimeField('Qual horário final para fechar a agenda?', auto_now=False, auto_now_add=False, default=time(00, 00))
    professionals = models.ManyToManyField(ProfessionalModel, related_name='close_professional', blank=True)
    description = models.CharField('Observações:', max_length=1000, null=True, blank=True)

    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.SET_NULL, blank=True)
    created_by = models.ForeignKey(User, related_name='close_schedule_user', on_delete=models.SET_NULL, blank=True, null=True)
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
        ordering = ["business"]
        constraints = [
            models.CheckConstraint(
                check=Q(start_date__lte=F('end_date'), start_hour__lte=F('end_hour')),
                name='close_start_before')
        ]
