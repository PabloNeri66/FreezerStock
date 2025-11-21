from django.urls import path
from .views import (
    GeladinhoListView, GeladinhoCreateView, GeladinhoDetailView,
    GeladinhoUpdateView, GeladinhoDeleteView,
    GeladinhoListCreateApiView, GeladinhoRetrieveUpdateDestroyApiView,
)

urlpatterns = [
    # Sistema
    path(
        'geladinhos/list/',
        GeladinhoListView.as_view(),
        name='geladinho_list',
    ),
    path(
        'geladinhos/create/',
        GeladinhoCreateView.as_view(),
        name='geladinho_create',
    ),
    path(
        'geladinhos/<int:pk>/detail/',
        GeladinhoDetailView.as_view(),
        name='geladinho_detail',
    ),
    path(
        'geladinhos/<int:pk>/update/',
        GeladinhoUpdateView.as_view(),
        name='geladinho_update',
    ),
    path(
        'geladinhos/<int:pk>/delete/',
        GeladinhoDeleteView.as_view(),
        name='geladinho_delete',
    ),

    # API
    path(
        'api/v1/geladinhos/',
        GeladinhoListCreateApiView.as_view(),
        name='geladinho-list-create-api-view',
    ),
    path(
        'api/v1/geladinhos/<int:pk>',
        GeladinhoRetrieveUpdateDestroyApiView.as_view(),
        name='geladinho-detail-api-view',
    )
]
