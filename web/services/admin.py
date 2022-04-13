from django.contrib import admin
from .models import (ServiceCategoryModel,
                     ServiceModel,
                     EquipmentModel,
                     ServiceEquipmentModel)
# Register your models here.


class EquipmentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['business']}),
        (None,               {'fields': ['title']}),
        (None,               {'fields': ['description']}),
        (None,               {'fields': ['qty']}),
        (None,               {'fields': ['is_active']}),
        (None,               {'fields': ['created_by']}),
    ]
    list_display = ('business', 'title', 'slug', 'is_active')
    list_filter = ['is_active']
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
    list_filter = ['is_active']
    search_fields = ['business', 'title']


admin.site.register(ServiceCategoryModel, ServiceCategoryAdmin)


class ServiceEquipmentAdmin(admin.StackedInline):

    model = ServiceEquipmentModel
    extra = 0
    fields = ['service', 'equipment', 'ept_time', 'ept_complement', 'ept_replaced', 'created_by']


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
    list_filter = ['is_active']
    search_fields = ['business', 'title']


admin.site.register(ServiceModel, ServiceAdmin)

