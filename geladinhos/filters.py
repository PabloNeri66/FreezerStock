import django_filters
from geladinhos.models import Geladinho


class GeladinhoFilter(django_filters.FilterSet):

    class Meta:
        model = Geladinho
        fields = {
            'flavor': ['exact'],
        }
