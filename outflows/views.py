from django.views.generic import (
    ListView, CreateView, DetailView,
)
from .models import Outflow
from core import metrics
from .forms import OutflowForm
from django.urls import reverse_lazy


class OutflowListView(ListView):
    model = Outflow
    template_name = 'outflow_list.html'
    context_object_name = 'outflows'
    paginate_by = 10

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


class OutflowCreateView(CreateView):
    model = Outflow
    template_name = 'outflow_create.html'
    form_class = OutflowForm
    success_url = reverse_lazy('outflow_list')


class OutflowDetailView(DetailView):
    model = Outflow
    template_name = 'outflow_detail.html'
