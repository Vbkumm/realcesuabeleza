from django.contrib import admin
from .models import (ServiceCategoryModel,
                     ServiceModel,
                     EquipmentAddressModel,
                     EquipmentModel,
                     ServiceEquipmentModel)
# Register your models here.


class EquipmentAddressAdmin(admin.StackedInline):
    raw_id_fields = ['address']
    model = EquipmentAddressModel
    extra = 0
    fieldsets = [
        (None,               {'fields': ['address']}),
        (None,               {'fields': ['equipment']}),
        (None,               {'fields': ['qty']}),
        (None,               {'fields': ['is_active']}),
        (None,               {'fields': ['updated_at']}),
        (None,               {'fields': ['updated_by']}),
        (None,               {'fields': ['created_by']}),
    ]


class EquipmentAdmin(admin.ModelAdmin):

    inlines = [EquipmentAddressAdmin, ]

    fieldsets = [
        (None,               {'fields': ['business']}),
        (None,               {'fields': ['title']}),
        (None,               {'fields': ['description']}),
        (None,               {'fields': ['created_by']}),
    ]
    list_display = ('business', 'title', 'slug')
    list_filter = ['business', 'title',]
    search_fields = ['business', 'title']


admin.site.register(EquipmentModel, EquipmentAdmin)


class ServiceCategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['business']}),
        (None,               {'fields': ['title']}),
        (None,               {'fields': ['is_active']}),
        (None,               {'fields': ['created_by']}),
    ]
    list_display = ('business', 'title', 'slug', 'is_active')
    list_filter = ['business', 'title', 'is_active']
    search_fields = ['business', 'title']


admin.site.register(ServiceCategoryModel, ServiceCategoryAdmin)


class ServiceEquipmentAdmin(admin.StackedInline):

    model = ServiceEquipmentModel
    extra = 0
    fields = ['service', 'equipment', 'equipment_time', 'equipment_complement', 'equipment_replaced', 'created_by']


class ServiceAdmin(admin.ModelAdmin):

    inlines = [
        ServiceEquipmentAdmin,
    ]

    fieldsets = [
        (None,               {'fields': ['business']}),
        (None,               {'fields': ['title']}),
        (None,               {'fields': ['description']}),
        (None,               {'fields': ['schedule_active']}),
        (None,               {'fields': ['cancel_schedule_active']}),
        (None,               {'fields': ['service_category']}),
        (None,               {'fields': ['is_active']}),
        (None,               {'fields': ['created_by']}),
        (None,               {'fields': ['_views']}),
    ]
    list_display = ('business', 'title', 'slug', 'is_active')
    list_filter = ['business', 'title', 'is_active']
    search_fields = ['business', 'title']


admin.site.register(ServiceModel, ServiceAdmin)

