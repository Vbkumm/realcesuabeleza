from django.contrib import admin
from .models import (ProfessionalCategoryModel,
                     ProfessionalModel,
                     ProfessionalUserModel,
                     ProfessionalAddressModel,
                     ProfessionalPhoneModel,
                     ProfessionalScheduleModel,
                     OpenScheduleModel,
                     CloseScheduleModel,
                     )


class ProfessionalCategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['business']}),
        (None,               {'fields': ['title']}),
        (None,               {'fields': ['is_active']}),
        (None,               {'fields': ['created_by']}),
    ]
    list_display = ('business', 'title', 'is_active')
    list_filter = ['is_active']
    search_fields = ['business', 'title']


admin.site.register(ProfessionalCategoryModel, ProfessionalCategoryAdmin)


class ProfessionalAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['business']}),
        (None,               {'fields': ['name']}),
        (None,               {'fields': ['began_date']}),
        (None,               {'fields': ['birth_date']}),
        (None,               {'fields': ['federal_id']}),
        (None,               {'fields': ['slug']}),
        (None,               {'fields': ['schedule_active']}),
        (None,               {'fields': ['cancel_schedule_active']}),
        (None,               {'fields': ['_views']}),
        (None,               {'fields': ['category']}),
        (None,               {'fields': ['is_active']}),
        (None,               {'fields': ['created_by']}),
    ]
    list_display = ('business', 'name', 'is_active')
    list_filter = ['is_active']
    search_fields = ['business', 'name']


admin.site.register(ProfessionalModel, ProfessionalAdmin)


class ProfessionalUserAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['user']}),
        (None,               {'fields': ['professional']}),
        (None,               {'fields': ['updated_at']}),
        (None,               {'fields': ['updated_by']}),
        (None,               {'fields': ['created_by']}),

    ]
    list_display = ('get_business', 'professional', 'user')
    list_filter = ['professional']
    search_fields = ['professional', 'user']

    def get_business(self, obj):
        return obj.professional.business


admin.site.register(ProfessionalUserModel, ProfessionalUserAdmin)


class ProfessionalAddressAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['professional']}),
        (None,               {'fields': ['zip_code']}),
        (None,               {'fields': ['street']}),
        (None,               {'fields': ['street_number']}),
        (None,               {'fields': ['district']}),
        (None,               {'fields': ['city']}),
        (None,               {'fields': ['state']}),
        (None,               {'fields': ['is_active']}),
        (None,               {'fields': ['updated_at']}),
        (None,               {'fields': ['updated_by']}),
        (None,               {'fields': ['created_by']}),
    ]
    list_display = ('get_business', 'professional', 'street', 'is_active')
    list_filter = ['is_active']
    search_fields = ['professional', 'street']

    def get_business(self, obj):
        return obj.professional.business


admin.site.register(ProfessionalAddressModel, ProfessionalAddressAdmin)


class ProfessionalPhoneAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['professional']}),
        (None,               {'fields': ['phone']}),
        (None,               {'fields': ['is_active']}),
        (None,               {'fields': ['updated_at']}),
        (None,               {'fields': ['updated_by']}),
        (None,               {'fields': ['created_by']}),
    ]
    list_display = ('get_business', 'professional', 'phone', 'is_active')
    list_filter = ['is_active']
    search_fields = ['professional', 'phone']

    def get_business(self, obj):
        return obj.professional.business


admin.site.register(ProfessionalPhoneModel, ProfessionalPhoneAdmin)


class ProfessionalScheduleAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['professional']}),
        (None,               {'fields': ['week_days']}),
        (None,               {'fields': ['start_hour']}),
        (None,               {'fields': ['end_hour']}),
        (None,               {'fields': ['fraction_time']}),
        (None,               {'fields': ['updated_at']}),
        (None,               {'fields': ['updated_by']}),
        (None,               {'fields': ['created_by']}),
    ]
    list_display = ('get_business', 'professional', 'week_days')
    list_filter = ['professional']
    search_fields = ['professional', 'week_days']

    def get_business(self, obj):
        return obj.professional.business


admin.site.register(ProfessionalScheduleModel, ProfessionalScheduleAdmin)


class OpenScheduleAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['business']}),
        (None,               {'fields': ['start_date']}),
        (None,               {'fields': ['end_date']}),
        (None,               {'fields': ['start_hour']}),
        (None,               {'fields': ['end_hour']}),
        (None,               {'fields': ['fraction_time']}),
        (None,               {'fields': ['professionals']}),
        (None,               {'fields': ['description']}),
        (None,               {'fields': ['updated_at']}),
        (None,               {'fields': ['updated_by']}),
        (None,               {'fields': ['created_by']}),
    ]
    list_display = ('business', 'start_date')
    list_filter = ['professionals']
    search_fields = ['professionals', 'business']


admin.site.register(OpenScheduleModel, OpenScheduleAdmin)


class CloseScheduleAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['business']}),
        (None,               {'fields': ['start_date']}),
        (None,               {'fields': ['end_date']}),
        (None,               {'fields': ['start_hour']}),
        (None,               {'fields': ['end_hour']}),
        (None,               {'fields': ['professionals']}),
        (None,               {'fields': ['description']}),
        (None,               {'fields': ['updated_at']}),
        (None,               {'fields': ['updated_by']}),
        (None,               {'fields': ['created_by']}),
    ]
    list_display = ('business', 'start_date')
    list_filter = ['professionals']
    search_fields = ['professionals', 'business']


admin.site.register(CloseScheduleModel, CloseScheduleAdmin)



