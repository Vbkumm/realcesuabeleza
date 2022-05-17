from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from lib.templatetags.validators import validate_file_extension
from django.utils.text import slugify
from .utils import img_creator, qr_code_generator


User = get_user_model()

# Create your models here.

#
# class BusinessManager(models.Manager):
#     pass


class BusinessModel(models.Model):
    title = models.CharField(max_length=150)
    logo_url = models.URLField(null=True)
    qrcode_img = models.FileField(upload_to='img/businesses_qr_code/', blank=True, null=True, validators=[validate_file_extension])
    slug = models.CharField(unique=True, max_length=150)
    email = models.EmailField(verbose_name='business email address', max_length=255, unique=True,)
    description = models.CharField('Descrição do salão*', max_length=1000, null=True, blank=True)
    birth_date = models.CharField('Data de criação do salão*',max_length=150, blank=True, null=True)
    federal_id = models.CharField(blank=True, max_length=15, null=True, unique=True, verbose_name='cnpj')
    owners = models.ManyToManyField(User, related_name='business_owners', blank=True)#donos do salao
    users = models.ManyToManyField(User, related_name='business_users', blank=True)#usuarios da plataforma q frequentam o salao
    is_active = models.BooleanField(default=True, help_text='Designates whether this business should be treated as active. Unselect this instead of deleting business.', verbose_name='business active')
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.SET_NULL, blank=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    #objects = BusinessManager()

    class Meta:
        verbose_name_plural = "business_list"
        verbose_name = "business"
        db_table = 'business_db'

    def get_absolute_url(self):
        return reverse("business_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):

        self.slug = slugify(self.slug).lower()
        self.qrcode_img = img_creator(qr_code_generator(self.get_absolute_url()))

        super(BusinessModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def __unicode__(self):

        return self.title

    def get_business_by_owner(self, user):

        return self.objects.get_queryset(owners__in=user)


class BusinessAddressModel(models.Model):
    business = models.ForeignKey(BusinessModel, related_name='business', on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True, help_text='Designates whether this address should be treated as active. Unselect this instead of deleting address.', verbose_name='address active')
    zip_code = models.CharField('CEP', max_length=9, null=True, blank=True)
    street = models.CharField('Rua', max_length=100, null=True, blank=True)
    street_number = models.CharField('Numero', max_length=100, null=True, blank=True)
    district = models.CharField('Bairro', max_length=100, null=True, blank=True)
    city = models.CharField('Cidade', max_length=100, null=True, blank=True)
    state = models.CharField('Estado', max_length=100, null=True, blank=True)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.SET_NULL, blank=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "business_address_list"
        verbose_name = "business_address"
        db_table = 'business_address_db'

    def __str__(self):
        return '%s %s' % (self.business, self.street)

    def get_address_by_business(self, business):
        return self.objects.get_queryset(business=business)

    def get_absolute_url(self):
        return reverse("business_address_detail", kwargs={"slug": self.business, "pk": self.pk})


def get_addresses_by_business(business=None):
    return BusinessAddressModel.objects.filter(business=business, is_active=True)


class BusinessPhoneModel(models.Model):
    address = models.ForeignKey(BusinessAddressModel, related_name='business_address_phone', on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True, help_text='Designates whether this phone should be treated as active. Unselect this instead of deleting phone.', verbose_name='phone active')
    phone = models.CharField('Telefone', max_length=150, null=True, blank=True)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.SET_NULL, blank=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "business_phone_list"
        verbose_name = "business_phone"
        db_table = 'business_phone_db'

    def __str__(self):
        return '%s %s' % (self.address, self.phone)

    def save(self, *args, **kwargs):
        numeric_filter = filter(str.isdigit, self.phone)
        numeric_string = "".join(numeric_filter)
        self.phone = numeric_string
        super(BusinessPhoneModel, self).save(*args, **kwargs)

    def get_phone_format(self):
        phone = self.phone
        phone = phone.lstrip('0')
        if len(phone) < 11:
            return f'({phone[0:2]}) {phone[2:6]}-{phone[6:]}'
        else:
            return f'({phone[0:2]}) {phone[2:7]}-{phone[7:]}'

    def get_phone_to_call(self):
        phone = self.phone
        phone = phone.lstrip('0')
        return phone

    def get_absolute_url(self):
        return reverse("businesses:address_phone_detail", kwargs={"pk": self.pk})


def get_phones_by_address(address=None):
    return BusinessPhoneModel.objects.filter(address=address, is_active=True)


def get_phones_by_addresses_by_business(business=None):
    addresses = get_addresses_by_business(business)
    address_and_phone = []
    if addresses:
        for address in addresses:
            phones = get_phones_by_address(address)
            address_and_phone.append([address, phones])

    return address_and_phone
