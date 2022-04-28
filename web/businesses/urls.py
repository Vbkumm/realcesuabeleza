from django.urls import path
from .views import BusinessViewSet


urlpatterns = [
    path('businesses', BusinessViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('businesses/<str:slug>', BusinessViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
]