from django.urls import path
from .views import (
    InflowListView,
    InflowCreateView,
    InflowDetailView,
    InflowListCreateApiView,
    InflowRetrieveApiView,
)

urlpatterns = [
    path(
        'inflows/list/',
        InflowListView.as_view(),
        name='inflow_list',
    ),
    path(
        'inflows/create/',
        InflowCreateView.as_view(),
        name='inflow_create',
    ),
    path(
        'inflows/<int:pk>/detail/',
        InflowDetailView.as_view(),
        name='inflow_detail',
    ),

    # API
    path(
        'api/v1/inflows/',
        InflowListCreateApiView.as_view(),
        name='inflow-list-create-api-view',
    ),
    path(
        'api/v1/inflows/<int:pk>/',
        InflowRetrieveApiView.as_view(),
        name='inflow-detail-api-view',
    ),
]