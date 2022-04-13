from django.contrib import admin
from .models import (CustomerModel,
                     CustomerUserModel,
                     CustomerAddressModel,
                     CustomerPhoneModel,
                     )

# Register your models here.


class CustomerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['business']}),
        (None,               {'fields': ['name']}),
        (None,               {'fields': ['is_active']}),
        (None,               {'fields': ['birth_date']}),
        (None,               {'fields': ['federal_id']}),
        (None,               {'fields': ['email']}),
        (None,               {'fields': ['receive_email']}),
        (None,               {'fields': ['updated_at']}),
        (None,               {'fields': ['updated_by']}),
        (None,               {'fields': ['created_by']}),
    ]
    list_display = ('business', 'name', 'is_active')
    list_filter = ['is_active']
    search_fields = ['business', 'name']


admin.site.register(CustomerModel, CustomerAdmin)


class CustomerUserAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['user']}),
        (None,               {'fields': ['customer']}),
        (None,               {'fields': ['updated_at']}),
        (None,               {'fields': ['updated_by']}),
        (None,               {'fields': ['created_by']}),

    ]
    list_display = ('get_business', 'get_customer', 'user')
    list_filter = ['customer']
    search_fields = ['customer', 'user']

    def get_business(self, obj):
        return obj.customer.business

    def get_customer(self, obj):
        return obj.customer.name


admin.site.register(CustomerUserModel, CustomerUserAdmin)


class CustomerAddressAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['customer']}),
        (None,               {'fields': ['zip_code']}),
        (None,               {'fields': ['street']}),
        (None,               {'fields': ['street_number']}),
        (None,               {'fields': ['district']}),
        (None,               {'fields': ['city']}),
        (None,               {'fields': ['state']}),
        (None,               {'fields': ['is_active']}),
    ]
    list_display = ('get_business', 'customer', 'is_active')
    list_filter = ['is_active']
    search_fields = ['customer', 'street']

    def get_business(self, obj):
        return obj.customer.business


admin.site.register(CustomerAddressModel, CustomerAddressAdmin)


class CustomerPhoneAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['customer']}),
        (None,               {'fields': ['phone']}),
        (None,               {'fields': ['is_active']}),
        (None,               {'fields': ['updated_at']}),
        (None,               {'fields': ['updated_by']}),
        (None,               {'fields': ['created_by']}),
    ]
    list_display = ('get_business', 'customer', 'phone', 'is_active')
    list_filter = ['is_active']
    search_fields = ['customer', 'phone']

    def get_business(self, obj):
        return obj.customer.business


admin.site.register(CustomerPhoneModel, CustomerPhoneAdmin)
