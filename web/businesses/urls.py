from django.urls import path
from .views import BusinessViewSet


urlpatterns = [
    path('api/', BusinessViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('api/<str:slug>', BusinessViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
]