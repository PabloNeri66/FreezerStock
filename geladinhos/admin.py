from django.contrib import admin
from .models import Geladinho


class GeladinhoAdmin(admin.ModelAdmin):
    list_display = (
        'flavor',
        'description',
        'cost_price',
        'selling_price',
        'quantity',
        'created_at',
        'updated_at',
    )
    search_fields = [
        'flavor',
    ]


admin.site.register(Geladinho, GeladinhoAdmin)