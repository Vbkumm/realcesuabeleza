from django.urls import path
from .views import (CustomerViewSet,
                    CustomerDetailView)


urlpatterns = [
    path('<str:slug>/customer/api/', CustomerViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('<str:slug>/customer/api/<int:pk>/', CustomerViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('<str:slug>/customer/<int:pk>/', CustomerDetailView.as_view(), name='customer_detail'),
]