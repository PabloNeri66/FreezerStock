import django_filters
from inflows.models import Inflow


class InflowFilter(django_filters.FilterSet):
    created_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Inflow
        fields = {
            'geladinho__flavor': ['exact'],
            'created_at': [],
        }
