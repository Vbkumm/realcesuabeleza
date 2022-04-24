from django.contrib import admin
from .models import ScheduleModel, ScheduleExtraTimeModel


class ScheduleExtraTimeAdmin(admin.StackedInline):

    model = ScheduleExtraTimeModel
    extra = 0
    fields = ['service_equipment', 'extra_time', 'updated_by', 'updated_at', 'created_by']


class ScheduleAdmin(admin.ModelAdmin):
    raw_id_fields = ['address', 'service', ]
    inlines = [
        ScheduleExtraTimeAdmin,
    ]

    fieldsets = [
        (None,               {'fields': ['address']}),
        (None,               {'fields': ['service']}),
        (None,               {'fields': ['customer']}),
        (None,               {'fields': ['professional']}),
        (None,               {'fields': ['date']}),
        (None,               {'fields': ['hour']}),
        (None,               {'fields': ['description']}),
        (None,               {'fields': ['_done']}),
        (None,               {'fields': ['_paid']}),
        (None,               {'fields': ['_canceled']}),
        (None,               {'fields': ['updated_at']}),
        (None,               {'fields': ['updated_by']}),
        (None,               {'fields': ['created_by']}),
    ]
    list_display = ('get_business', 'address', 'service', 'professional')
    list_filter = ['address', 'customer', 'professional']
    search_fields = ['address', 'service']

    def get_business(self, obj):
        return obj.address.business


admin.site.register(ScheduleModel, ScheduleAdmin)


