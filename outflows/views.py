from django.views.generic import (
    ListView, CreateView, DetailView,
)
from rest_framework.generics import (
    ListCreateAPIView, RetrieveAPIView,
)
from .serializers import OutflowSerializer
from .models import Outflow
from core import metrics
from .forms import OutflowForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)


class OutflowListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Outflow
    template_name = 'outflow_list.html'
    context_object_name = 'outflows'
    paginate_by = 10
    permission_required = 'outflows.view_outflow'

    def get_queryset(self):
        """Filtragem por Nome"""
        queryset = super().get_queryset().defer('description')
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
    queryset = Outflow.objects.all()
    serializer_class = OutflowSerializer


class OutflowRetrieveApiView(RetrieveAPIView):
    queryset = Outflow.objects.all()
    serializer_class = OutflowSerializer
