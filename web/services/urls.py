from django.urls import path
from .views import (ServiceViewSet,
                    ServiceDetailView,
                    ServiceCategoryViewSet,
                    ServiceCategoryDetailView)


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

    path('service_category/api/', ServiceCategoryViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('service_category/api/<str:slug>', ServiceCategoryViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('<slug>/service/<service_category_slug>/', ServiceCategoryDetailView.as_view(), name='service_category_detail'),

]