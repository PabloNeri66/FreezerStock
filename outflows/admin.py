from django.contrib import admin
from .models import Outflow


class OutflowAdmin(admin.ModelAdmin):
    list_display = (
        'geladinho',
        'quantity',
        'description',
        'created_at',
        'updated_at',
    )
    search_fields = (
        'geladinho',
    )


admin.site.register(Outflow, OutflowAdmin)