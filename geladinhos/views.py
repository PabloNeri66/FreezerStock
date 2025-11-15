# Create your views here.
from django.views.generic import (
    ListView, CreateView, DetailView, UpdateView, DeleteView,
)
from .models import Geladinho
from core import metrics
from .forms import GeladinhoForm
from django.urls import reverse_lazy


class GeladinhoListView(ListView):
    model = Geladinho
    template_name = 'geladinho_list.html'
    context_object_name = 'geladinhos'
    paginate_by = 10

    def get_queryset(self):
        """Filtragem por Nome"""
        queryset = super().get_queryset()
        flavor = self.request.GET.get('flavor')

        if flavor:
            queryset = queryset.filter(flavor__icontains=flavor)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["geladinho_metrics"] = metrics.get_geladinho_metrics()
        return context


class GeladinhoCreateView(CreateView):
    model = Geladinho
    template_name = 'geladinho_create.html'
    form_class = GeladinhoForm
    success_url = reverse_lazy('geladinho_list')


class GeladinhoDetailView(DetailView):
    model = Geladinho
    template_name = 'geladinho_detail.html'


class GeladinhoUpdateView(UpdateView):
    model = Geladinho
    template_name = 'geladinho_update.html'
    form_class = GeladinhoForm
    success_url = reverse_lazy('geladinho_list')


class GeladinhoDeleteView(DeleteView):
    model = Geladinho
    template_name = 'geladinho_delete.html'
    success_url = reverse_lazy('geladinho_list')
