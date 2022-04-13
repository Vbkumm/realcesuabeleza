from django.contrib import admin
from .models import ServiceCategoryModel, ServiceModel
# Register your models here.


class ServiceCategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['business']}),
        (None,               {'fields': ['title']}),
        (None,               {'fields': ['is_active']}),
        (None,               {'fields': ['created_by']}),
    ]
    list_display = ('business', 'title', 'slug', 'is_active')
    list_filter = ['is_active']
    search_fields = ['business', 'name']


admin.site.register(ServiceCategoryModel, ServiceCategoryAdmin)


class ServiceAdmin(admin.ModelAdmin):
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

