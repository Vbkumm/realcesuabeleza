from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from lib.templatetags.validators import validate_file_extension
from django.dispatch import receiver
from django.db.models.signals import post_save
from PIL import Image
from io import BytesIO, StringIO
from django.core.files.base import ContentFile
import webp
from django.utils.text import slugify
from .utils import (qr_code_generator,
                    get_logo_img,
                    get_favicon,
                    get_logo_rgb)


User = get_user_model()


class BusinessManager(models.Manager):

    def get_new_business_user(self, user, slug):
        business = self.get_queryset().get(slug=slug,)
        if user not in business.users.all():
            business.users.add(user)
            business.save()
        return business


class BusinessModel(models.Model):
    title = models.CharField(max_length=150)
    logo_url = models.URLField(null=True)
    logo_img = models.FileField(upload_to='img/businesses_logo/', blank=True, null=True, validators=[validate_file_extension])
    logo_rgb_color = models.CharField(max_length=150, null=True)
    favicon = models.FileField(upload_to='img/businesses_favicon/', blank=True, null=True, validators=[validate_file_extension])
    qrcode_img = models.FileField(upload_to='img/businesses_qr_code/', blank=True, null=True, validators=[validate_file_extension])
    slug = models.CharField(unique=True, max_length=150)
    email = models.EmailField(verbose_name='business email address', max_length=255, unique=True,)
    description = models.CharField('Descrição do salão*', max_length=1000, null=True, blank=True)
    birth_date = models.CharField('Data de criação do salão*',max_length=150, blank=True, null=True)
    federal_id = models.CharField(blank=True, max_length=20, null=True, verbose_name='cnpj')
    owners = models.ManyToManyField(User, related_name='business_owners', blank=True)#donos do salao
    users = models.ManyToManyField(User, related_name='business_users', blank=True)#usuarios da plataforma q frequentam o salao
    is_active = models.BooleanField(default=True, help_text='Designates whether this business should be treated as active. Unselect this instead of deleting business.', verbose_name='business active')
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.SET_NULL, blank=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = BusinessManager()

    class Meta:
        verbose_name_plural = "business_list"
        verbose_name = "business"
        db_table = 'business_db'

    def get_absolute_url(self):
        return reverse("business_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):

        self.slug = slugify(self.slug).lower()
        icon_io = BytesIO()
        thumb_io = BytesIO()
        qrcode_io = BytesIO()
        if self.logo_img:
            logo_img = get_logo_img(self.logo_img)
            logo_img.save(thumb_io, format='JPEG', quality=100)
            rgb = get_logo_rgb(logo_img)
            self.logo_rgb_color = rgb
            qr_code_img = qr_code_generator(self.slug, rgb)
            logo_img = get_logo_img(self.logo_img)
            logo_pos = ((qr_code_img.size[0] - logo_img.size[0]) // 2, (qr_code_img.size[1] - logo_img.size[1]) // 2)
            qr_code_img.paste(logo_img, logo_pos)
            webp.save_image(logo_img, self.slug + ".webp", quality=99)
            self.logo_img.save(self.slug + ".webp", ContentFile(thumb_io.getvalue()), save=False)
            favicon = get_favicon(self.logo_img)
            favicon.save(icon_io, format='JPEG', quality=80)
            self.favicon.save(self.slug + ".ico", ContentFile(icon_io.getvalue()), save=False)
        else:
            qr_code_img = qr_code_generator(self.slug)
        qr_code_img.save(qrcode_io, format='JPEG', quality=100)
        self.qrcode_img.save(self.slug + ".webp", ContentFile(qrcode_io.getvalue()), save=False)

        super(BusinessModel, self).save(*args, **kwargs)

    @receiver(post_save, sender=User)
    def set_business_users(sender, instance, **kwargs):
        if instance.business:
            if BusinessModel.objects.filter(slug=instance.business):
                business = BusinessModel.objects.get(slug=instance.business)
                if instance not in business.users.all():
                    business.users.add(instance)
                business.save()

    def __str__(self):
        return self.title

    def __unicode__(self):

        return self.title

    def get_qr_code(self):
        return qr_code_generator(self.slug)

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

