from django.views.generic import (
    ListView, CreateView, DetailView, UpdateView, DeleteView,
)
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView,
)
from .serializers import GeladinhoSerializer
from .models import Geladinho
from core import metrics, permissions
from .forms import GeladinhoForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)


class GeladinhoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Geladinho
    template_name = 'geladinho_list.html'
    context_object_name = 'geladinhos'
    paginate_by = 10
    permission_required = 'geladinhos.view_geladinho'  # app.Djangomethod_model

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


class GeladinhoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Geladinho
    template_name = 'geladinho_create.html'
    form_class = GeladinhoForm
    success_url = reverse_lazy('geladinho_list')
    permission_required = 'geladinhos.add_geladinho'


class GeladinhoDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Geladinho
    template_name = 'geladinho_detail.html'
    permission_required = 'geladinhos.view_geladinho'


class GeladinhoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Geladinho
    template_name = 'geladinho_update.html'
    form_class = GeladinhoForm
    success_url = reverse_lazy('geladinho_list')
    permission_required = 'geladinhos.change_geladinho'


class GeladinhoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Geladinho
    template_name = 'geladinho_delete.html'
    success_url = reverse_lazy('geladinho_list')
    permission_required = 'geladinhos.view_geladinho'


# API VIEWS
class GeladinhoListCreateApiView(ListCreateAPIView):
    queryset = Geladinho.objects.all()
    serializer_class = GeladinhoSerializer
    permission_classes = [permissions.GlobalDefaultPermission]


class GeladinhoRetrieveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
    queryset = Geladinho.objects.all()
    serializer_class = GeladinhoSerializer
    permission_classes = [permissions.GlobalDefaultPermission]

