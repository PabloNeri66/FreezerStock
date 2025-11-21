from django.urls import path
from .views import (
    OutflowListView,
    OutflowCreateView,
    OutflowDetailView,
    OutflowListCreateApiView,
    OutflowRetrieveApiView,
)

urlpatterns = [
    path(
        'outflows/list/',
        OutflowListView.as_view(),
        name='outflow_list',
    ),
    path(
        'outflows/create/',
        OutflowCreateView.as_view(),
        name='outflow_create',
    ),
    path(
        'outflows/<int:pk>/detail/',
        OutflowDetailView.as_view(),
        name='outflow_detail',
    ),

    # API
    path(
        'api/v1/outflows/',
        OutflowListCreateApiView.as_view(),
        name='outflow-list-create-api-view',
    ),
    path(
        'api/v1/outflows/<int:pk>/',
        OutflowRetrieveApiView.as_view(),
        name='outflow-detail-api-view',
    ),
]
