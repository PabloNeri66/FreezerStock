# Django
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
)
# Django Filters
from django_filters.rest_framework import DjangoFilterBackend
# Django REST Framework
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveAPIView,
)

# Core / projeto
from core import metrics, permissions

# App local
from .forms import OutflowForm
from .models import Outflow
from .serializers import OutflowSerializer
from .filters import OutflowFilter


class OutflowListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Outflow
    template_name = 'outflow_list.html'
    context_object_name = 'outflows'
    paginate_by = 10
    permission_required = 'outflows.view_outflow'

    def get_queryset(self):
        """Filtragem por Nome"""
        queryset = super().get_queryset().select_related('geladinho')
        geladinho = self.request.GET.get('geladinho')

        if geladinho:
            queryset = queryset.filter(geladinho__flavor__icontains=geladinho)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sales_metrics'] = metrics.get_sales_metrics()
        return context


class OutflowCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Outflow
    template_name = 'outflow_create.html'
    form_class = OutflowForm
    success_url = reverse_lazy('outflow_list')
    permission_required = 'outflows.add_outflow'


class OutflowDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Outflow
    template_name = 'outflow_detail.html'
    permission_required = 'outflows.detail_outflow'


# API
class OutflowListCreateApiView(ListCreateAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = OutflowFilter
    queryset = Outflow.objects.all()
    serializer_class = OutflowSerializer
    permission_classes = [permissions.GlobalDefaultPermission]

    # @method_decorator(cache_page(60 * 15, key_prefix='outflow_list'))
    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)


class OutflowRetrieveApiView(RetrieveAPIView):
    queryset = Outflow.objects.all()
    serializer_class = OutflowSerializer
    permission_classes = [permissions.GlobalDefaultPermission]