from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUserModel


class CustomUserAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['email']}),
        (None,               {'fields': ['phone']}),
        (None,               {'fields': ['is_active']}),
        (None,               {'fields': ['is_staff']}),
    ]
    list_display = ('email', 'phone', 'is_active')
    list_filter = ['is_active']
    search_fields = ['username', 'email']


admin.site.register(CustomUserModel, CustomUserAdmin)

