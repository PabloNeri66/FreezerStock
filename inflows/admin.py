from django.contrib import admin
from .models import Inflow


class InflowAdmin(admin.ModelAdmin):
    list_display = (
        'geladinho',
        'quantity',
        'manufacturing_date',
        'created_at',
        'updated_at',
    )
    search_fields = (
        'geladinho',
    )


admin.site.register(Inflow, InflowAdmin)
