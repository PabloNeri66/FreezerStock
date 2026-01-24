import django_filters
from outflows.models import Outflow


class OutflowFilter(django_filters.FilterSet):
    created_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Outflow
        fields = {
            'geladinho__flavor': ['exact'],
            'created_at': [],
        }
