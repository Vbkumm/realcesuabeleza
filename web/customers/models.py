from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.validators import validate_email
#from service.models import ServiceModel
from businesses.models import BusinessModel


User = get_user_model()


# Create your models here.


class CustomerModel(models.Model):

    business = models.ForeignKey(BusinessModel, related_name='customer_business', on_delete=models.CASCADE,)
    name = models.CharField('Qual nome da Cliente*',max_length=150, unique=True)
    is_active = models.BooleanField(default=True, help_text='Designates whether this customer should be treated as active. Unselect this instead of deleting customer.', verbose_name='customer active')
    birth_date = models.CharField('Data de nascimento*',max_length=150, blank=True, null=True)
    federal_id = models.CharField('CNPJ ou CPF', max_length=15, unique=True, blank=True, null=True)
    email = models.EmailField('E-mail', max_length=254, null=True, blank=False, validators=[validate_email])
    receive_email = models.BooleanField('Marque para bloquear emails automaticos', default=False)
    schedule_active = models.BooleanField('Cliente credenciada ao agendamento online', default=False)
    #self_booking_service_off = models.ManyToManyField(ServiceModel, related_name='customer_self_book_service_off')
    #self_booking_service_off = models.ManyToManyField(ServiceModel, related_name='customer_self_unbook_service_off')
    updated_at = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='+',on_delete=models.SET_NULL, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "customer_list"
        verbose_name = "customer"
        db_table = 'customer_db'
        ordering = ['business', 'name', ]

    def __str__(self):
        return '%s %s %s' % (self.pk, self.name, self.business)

    def get_absolute_url(self):

        return reverse('customer_detail', kwargs={"slug": self.business.slug, 'pk': self.pk})

    def get_customer_by_business(self, business):
        return self.objects.get_queryset(business=business)


class CustomerUserModel(models.Model):

    """Correlaciona usuario do app a cadastro de clientes do salão"""

    user = models.ForeignKey(User, related_name='user_customer', on_delete=models.CASCADE)
    customer = models.OneToOneField(CustomerModel, related_name='customer_user', on_delete=models.CASCADE)

    updated_at = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='+',on_delete=models.SET_NULL, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)


class CustomerAddressModel(models.Model):
    """
    Endereço residencial do cliente do salao
    """
    customer = models.ForeignKey(CustomerModel, related_name='customer_address', on_delete=models.CASCADE, null=True, blank=True)
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
        verbose_name_plural = "customer_address_list"
        verbose_name = "customer_address"
        db_table = 'customer_address_db'
        ordering = ['customer',]

    def __str__(self):
        return '%s %s' % (self.customer, self.street)

    def get_address_by_customer(self, customer):
        return self.objects.get_queryset(customer=customer)


class CustomerPhoneModel(models.Model):
    customer = models.ForeignKey(CustomerModel, related_name='customer_phone', on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField('Telefone', max_length=150, null=True, blank=True)
    is_active = models.BooleanField(default=True, help_text='Designates whether this address should be treated as active. Unselect this instead of deleting address.', verbose_name='phone active')

    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.SET_NULL, blank=True)
    created_by = models.ForeignKey(User, related_name='customer_phone_author', on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "customer_phone_list"
        verbose_name = "customer_phone"
        db_table = 'customer_phone_db'
        ordering = ['customer']

    def __str__(self):
        return '%s %s' % (self.customer, self.phone)

    def get_phone_by_customer(self, customer):
        return self.objects.get_queryset(customer=customer)

