from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.html import mark_safe
from markdown import markdown
from django.utils.text import slugify
from businesses.models import BusinessModel
from .utils import _generate_unique_slug


# Create your models here.

User = get_user_model()


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

    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    business = models.ForeignKey(BusinessModel, related_name='category_professional_business', on_delete=models.CASCADE,)
    title = models.CharField('Título*', max_length=150)
    slug = models.CharField(unique=True, max_length=150)
    description = models.CharField('Descrição*', max_length=1000, null=True, blank=True)
    is_active = models.BooleanField(default=True, help_text='Designates whether this service should be treated as active. Unselect this instead of deleting service.', verbose_name='business service active')
    schedule_active = models.BooleanField('Permitir que o cliente agende online', default=False)
    cancel_schedule_active = models.BooleanField('Permitir que o cliente cancele o agendamento feito por ele online', default=False)
    service_category = models.ForeignKey(ServiceCategoryModel, related_name='service_category', on_delete=models.SET_NULL, blank=True, null=True)
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
        return mark_safe(markdown(self.service_description, safe_mode='escape'))

    def save(self, *args, **kwargs):
        self.slug = _generate_unique_slug(self)
        super(ServiceModel, self).save(*args, **kwargs)



