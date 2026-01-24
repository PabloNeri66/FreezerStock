from django.views.generic import (
    ListView, CreateView, DetailView,
)
from django.urls import reverse_lazy
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from rest_framework.generics import (
    ListCreateAPIView, RetrieveAPIView,
)

from core import permissions
from .filters import InflowFilter
from .forms import InflowForm
from .models import Inflow
from .serializers import InflowSerializer


class InflowListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Inflow
    template_name = 'inflow_list.html'
    context_object_name = 'inflows'
    paginate_by = 10
    permission_required = 'inflows.view_inflow'

    def get_queryset(self):
        """Filtragem por Nome"""
        queryset = super().get_queryset()
        geladinho = self.request.GET.get('geladinho')

        if geladinho:
            queryset = queryset.filter(geladinho__flavor__icontains=geladinho)
        return queryset


class InflowCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Inflow
    template_name = 'inflow_create.html'
    form_class = InflowForm
    success_url = reverse_lazy('inflow_list')
    permission_required = 'inflows.add_inflow'


class InflowDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Inflow
    template_name = 'inflow_detail.html'
    permission_required = 'inflows.detail_inflow'


# API
class InflowListCreateApiView(ListCreateAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = InflowFilter
    queryset = Inflow.objects.all()
    serializer_class = InflowSerializer
    permission_classes = [permissions.GlobalDefaultPermission]


class InflowRetrieveApiView(RetrieveAPIView):
    queryset = Inflow.objects.all()
    serializer_class = InflowSerializer
    permission_classes = [permissions.GlobalDefaultPermission]
