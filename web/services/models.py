from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils.duration import _get_duration_components
from django.urls import reverse
from django.utils.html import mark_safe
from markdown import markdown
from businesses.models import BusinessModel, BusinessAddressModel
from professionals.utils import _generate_unique_slug


# Create your models here.

User = get_user_model()


class EquipmentModel(models.Model):
    """
    Cadastro de equipamentos para realizar o serviço no salao
    """
    business = models.ForeignKey(BusinessModel, related_name='business_equipment', on_delete=models.CASCADE,)
    title = models.CharField('Tipo de equipamento*', max_length=150)
    slug = models.CharField(unique=True, max_length=150)
    description = models.CharField('Descrição*', max_length=1000, null=True, blank=True)
    addresses = models.ManyToManyField(BusinessAddressModel, related_name='equipment_address', blank=True, through="EquipmentAddressModel")

    updated_at = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.SET_NULL, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "equipment_list"
        verbose_name = "equipments"
        db_table = 'equipments_db'

    def __str__(self):

        return '%s %s' % (self.title, self.addresses)

    def get_description_as_markdown(self):
        return mark_safe(markdown(self.description, safe_mode='escape'))

    def save(self, *args, **kwargs):
        self.slug = _generate_unique_slug(self)
        super(EquipmentModel, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('equipments:detail',  kwargs={"slug": self.slug})


class EquipmentAddressModel(models.Model):
    """
    Cadastra equipamento por endereço do salao
    """

    CHOICES = [(i, i) for i in range(1, 51)]
    address = models.ForeignKey(BusinessAddressModel, related_name='equipment_business_address', on_delete=models.CASCADE, null=True, blank=True)
    equipment = models.ForeignKey(EquipmentModel, related_name='equipment_address', on_delete=models.CASCADE, null=True, blank=True)
    qty = models.IntegerField('Quantidade deste equipamento?', choices=CHOICES, default=1)
    is_active = models.BooleanField(default=True, help_text='Designates whether this equipments should be treated as active. Unselect this instead of deleting equipments.', verbose_name='business equipments active')

    updated_at = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.SET_NULL, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "equipment_address_list"
        verbose_name = "equipment_address"
        db_table = 'equipment_address_db'

    def __str__(self):

        return '%s %s %s' % (self.equipment, self.qty, self.address)


class ServiceCategoryModel(models.Model):
    """
    Categoria de serviços fica relacionada a categoria de profissional que a executa e ao salão
    """
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    business = models.ForeignKey(BusinessModel, related_name='business_service_category', on_delete=models.CASCADE,)
    title = models.CharField('Qual nova categoria de serviços?', max_length=100,)
    slug = models.CharField(unique=True, max_length=150)
    is_active = models.BooleanField(default=True, help_text='Designates whether this service category should be treated as active. Unselect this instead of deleting service category.', verbose_name='business service category active')
    updated_at = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.SET_NULL, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "service_category_list"

    def __str__(self):
        return '%s %s %s' % (self.pk, self.title, self.business)

    def save(self, *args, **kwargs):
        self.slug = _generate_unique_slug(self)
        super(ServiceCategoryModel, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('services:category',  kwargs={"slug": self.slug})


class ServiceQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (Q(service_tittle__icontains=query) |
                         Q(service_description__icontains=query)
                         )

            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs


class ServiceManager(models.Manager):

    def get_queryset(self):
        return ServiceQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset()


class ServiceModel(models.Model):
    """
    Cadastros dos servicos realizados no salao separados por categoria de servico
    """
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    business = models.ForeignKey(BusinessModel, related_name='category_professional_business', on_delete=models.CASCADE,)
    title = models.CharField('Título*', max_length=150)
    slug = models.CharField(unique=True, max_length=150)
    description = models.CharField('Descrição*', max_length=1000, null=True, blank=True)
    is_active = models.BooleanField(default=True, help_text='Designates whether this service should be treated as active. Unselect this instead of deleting service.', verbose_name='business service active')
    schedule_active = models.BooleanField('Permitir que o cliente agende online', default=False)
    cancel_schedule_active = models.BooleanField('Permitir que o cliente cancele o agendamento feito por ele online', default=False)
    service_category = models.ForeignKey(ServiceCategoryModel, related_name='service_category', on_delete=models.SET_NULL, blank=True, null=True)
    equipments = models.ManyToManyField(EquipmentModel, blank=True, through_fields=('service', 'equipment'), through="ServiceEquipmentModel")
    updated_at = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.SET_NULL, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    _views = models.PositiveIntegerField(default=0)

    objects = ServiceManager()

    class Meta:
        verbose_name_plural = "service_list"
        verbose_name = "services"
        db_table = 'service_db'

    def __str__(self):
        return '%s %s %s' % (self.pk, self.title, self.business)

    def get_absolute_url(self):
        return reverse('services:detail',  kwargs={"slug": self.slug})

    def get_description_as_markdown(self):
        return mark_safe(markdown(self.description, safe_mode='escape'))

    def save(self, *args, **kwargs):
        self.slug = _generate_unique_slug(self)
        super(ServiceModel, self).save(*args, **kwargs)

    def get_service_by_business(self, business):
        return self.objects.get_queryset(business=business)

    def get_total_time_service(self):

        equipment_list = self.equipments


class ServiceEquipmentModel(models.Model):
    """
    Conecta equipamentos necessarios para realizar o servico no salao
    """
    service = models.ForeignKey(ServiceModel, related_name='service', on_delete=models.CASCADE)
    equipment = models.ForeignKey(EquipmentModel, related_name='equipment', on_delete=models.CASCADE)
    ept_time = models.IntegerField('Qual tempo em minutos de uso deste equipamento?', default=0)
    ept_complement = models.BooleanField('Este equipamento é usado simutaniamente com algum outro equipamento?',default=False)
    ept_replaced = models.ForeignKey(EquipmentModel, related_name='equipment_replaced', on_delete=models.CASCADE, null=True, blank=True)

    updated_at = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.SET_NULL, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "service_equipment_list"
        verbose_name = "service_equipments"
        db_table = 'service_equipments_db'

    def __str__(self):
        return '%s %s %s %s %s' % (self.service, self.equipment, self.ept_time, self.ept_complement, self.ept_replaced)

    def get_equipments_by_service(self, service):
        return self.objects.get_queryset(service=service)

    def get_service_equipment_time(self, address=None, service=None, equipments_extra_time=None):
        """
        Retorna tempo de uso do equipamento para execução do serviço se nao for usado como complementar ou substituto.
        """
        service_total_time = 0
        equipments_extra_time = equipments_extra_time
        equipment_qty_and_time = []
        final_equipment_list_by_service = []
        equipment_service_list = self.objects.get_queryset(service=service)
        for equipment_service in equipment_service_list:
            equipment_time = equipment_service.ept_time
            if equipments_extra_time:
                for extra_time in equipments_extra_time:
                    if extra_time.service_equipment == equipment_service:
                        equipment_time += extra_time.extra_time

            equipment_replaced_list = self.objects.get_queryset(service=service, ept_replaced=equipment_service.equipment)
            equipment_qtd_address = EquipmentAddressModel.objects.filter(address=address, equipment=equipment_service.equipment).first()
            equipment_qtd = equipment_qtd_address.qty
            if equipment_replaced_list:
                for equipment_replaced in equipment_replaced_list:
                    equipment_replaced_qtd_address = EquipmentAddressModel.objects.filter(address=address, equipment=equipment_replaced.equipment).first()
                    equipment_replaced_qtd = equipment_replaced_qtd_address.qty
                    equipment_qtd += equipment_replaced_qtd

            if not equipment_service.ept_complement or equipment_service.ept_replaced:
                service_total_time += equipment_time

            equipment_qty_and_time.append([address, equipment_service, equipment_qtd, equipment_service.ept_complement, equipment_service.ept_replaced])

        return final_equipment_list_by_service.append([service_total_time, equipment_qty_and_time])
