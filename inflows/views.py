from django.views.generic import (
    ListView, CreateView, DetailView,
)
from .models import Inflow
from .forms import InflowForm
from django.urls import reverse_lazy


class InflowListView(ListView):
    model = Inflow
    template_name = 'inflow_list.html'
    context_object_name = 'inflows'
    paginate_by = 10

    def get_queryset(self):
        """Filtragem por Nome"""
        queryset = super().get_queryset().defer('description')
        geladinho = self.request.GET.get('geladinho')

        if geladinho:
            queryset = queryset.filter(geladinho__flavor__icontains=geladinho)
        return queryset


class InflowCreateView(CreateView):
    model = Inflow
    template_name = 'inflow_create.html'
    form_class = InflowForm
    success_url = reverse_lazy('inflow_list')


class InflowDetailView(DetailView):
    model = Inflow
    template_name = 'inflow_detail.html'