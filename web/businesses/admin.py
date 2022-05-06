from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (BusinessModel,
                     BusinessAddressModel,
                     BusinessPhoneModel)


class BusinessAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['title']}),
        (None,               {'fields': ['slug']}),
        (None,               {'fields': ['email']}),
        (None,               {'fields': ['logo_url']}),
        (None,               {'fields': ['description']}),
        (None,               {'fields': ['birth_date']}),
        (None,               {'fields': ['federal_id']}),
        (None,               {'fields': ['owners']}),
        (None,               {'fields': ['users']}),
        (None,               {'fields': ['is_active']}),
        (None,               {'fields': ['updated_by']}),
        (None,               {'fields': ['updated_at']}),
        (None,               {'fields': ['created_by']}),
    ]
    list_display = ('title', 'email', 'is_active')
    list_filter = ['is_active']
    search_fields = ['title', 'email']


admin.site.register(BusinessModel, BusinessAdmin)


class BusinessAddressAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['business']}),
        (None,               {'fields': ['zip_code']}),
        (None,               {'fields': ['street']}),
        (None,               {'fields': ['street_number']}),
        (None,               {'fields': ['district']}),
        (None,               {'fields': ['city']}),
        (None,               {'fields': ['state']}),
        (None,               {'fields': ['updated_by']}),
        (None,               {'fields': ['updated_at']}),
        (None,               {'fields': ['created_by']}),

    ]
    list_display = ('business', 'zip_code', 'street', 'is_active')
    list_filter = ['business']
    search_fields = ['business', 'zip_code']


admin.site.register(BusinessAddressModel, BusinessAddressAdmin)


class BusinessPhoneAdmin(admin.ModelAdmin):
    raw_id_fields = ['address']
    fieldsets = [
        (None,               {'fields': ['address']}),
        (None,               {'fields': ['phone']}),
        (None,               {'fields': ['updated_by']}),
        (None,               {'fields': ['updated_at']}),
        (None,               {'fields': ['created_by']}),

    ]

    list_display = ('get_business', 'phone', 'get_address', 'is_active')
    list_filter = ['address__street', 'address__business']
    search_fields = ['get_business', 'get_address', 'phone']

    def get_business(self, obj):
        return obj.address.business

    def get_address(self, obj):
        return obj.address.street


admin.site.register(BusinessPhoneModel, BusinessPhoneAdmin)

