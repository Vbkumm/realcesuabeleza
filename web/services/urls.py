from django.urls import path
from .views import ServiceViewSet, ServiceDetailView


urlpatterns = [
    path('service/api/', ServiceViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('service/api/<str:slug>', ServiceViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('<slug>/service/<service_slug>/', ServiceDetailView.as_view(), name='service_detail'),

]