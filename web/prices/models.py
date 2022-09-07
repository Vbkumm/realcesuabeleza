from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from model_utils import FieldTracker
from services.models import ServiceModel, get_service_equipment_time_list


User = get_user_model()


class PriceModel(models.Model):
    value = models.DecimalField('Qual valor?', max_digits=10, decimal_places=2, null=True, blank=True)
    old_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    service = models.OneToOneField(ServiceModel, related_name='price_service', on_delete=models.CASCADE, null=True, blank=True)
    #combo = models.OneToOneField(ComboModel, related_name='price_combo', on_delete=models.CASCADE, null=True, blank=True)
    #product = models.OneToOneField(ProductModel, related_name='price_product', on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField('Preço visisvel?', default=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.SET_NULL, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    value_tracker = FieldTracker(fields=['value'])

    def save(self, *args, **kwargs):
        if not self.value:
            self.value = self.value
            self.old_value = self.value_tracker.previous('value')

        super(PriceModel, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.service) + ": R$ " + str(self.value)

    class Meta:
        verbose_name_plural = "price_list"
        verbose_name = "price"
        db_table = 'price_db'

    def get_absolute_url(self):
        return reverse('price_detail', kwargs={'pk': self.pk})

    @receiver(post_save, sender=ServiceModel)
    def get_price_service_create(sender, instance, created,  **kwargs):
        if created:
            service_created_by = instance.created_by
            PriceModel.objects.create(service=instance, created_by=service_created_by, created=timezone.now())
            instance.save()

    # @receiver(post_save, sender=ComboModel)
    # def get_price_combo_create(sender, instance, created,  **kwargs):
    #     if created:
    #         combo_author = instance.combo_author
    #
    #         PriceModel.objects.create(price_combo=instance, price_user=combo_author)
    #         instance.combo_author.save()
    #
    # @receiver(post_save, sender=ProductModel)
    # def get_price_product_create(sender, instance, created,  **kwargs):
    #     if created:
    #         author = instance.author
    #
    #         PriceModel.objects.create(price_product=instance, price_user=author)
    #         instance.author.save()


def get_service_equipment_time_and_price_in_list(business, service_category):
    service_list = get_service_equipment_time_list(business, service_category)
    return [[i[0], i[1], PriceModel.objects.filter(service=i[0]).first()] for i in service_list]
