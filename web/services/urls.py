from django.urls import path
from .views import (ServiceViewSet,
                    ServiceDetailView,
                    ServiceCategoryViewSet,
                    ServiceCategoryDetailView,
                    EquipmentViewSet,
                    EquipmentDetailView,
                    ServiceEquipmentViewSet,
                    ServiceEquipmentDetailView,
                    EquipmentAddressViewSet,
                    EquipmentAddressDetailView)


urlpatterns = [
    path('<str:slug>/service/api/', ServiceViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('<str:slug>/service/api/<str:service_slug>/', ServiceViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('<str:slug>/service/<str:service_slug>/', ServiceDetailView.as_view(), name='service_detail'),


    path('<str:slug>/service_category/api/', ServiceCategoryViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('<str:slug>/service_category/api/<str:service_category_slug>/', ServiceCategoryViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('<str:slug>/service_category/<str:service_category_slug>/', ServiceCategoryDetailView.as_view(), name='service_category_detail'),


    path('<str:slug>/equipment/api/', EquipmentViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('<str:slug>/equipment/api/<str:equipment_slug>/', EquipmentViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('<str:slug>/equipment/<str:equipment_slug>/', EquipmentDetailView.as_view(), name='equipment_detail'),


    path('<str:slug>/service_equipment/api/', ServiceEquipmentViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('<str:slug>/service_equipment/api/<int:pk>/', ServiceEquipmentViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('<str:slug>/service_equipment/<int:pk>/', ServiceEquipmentDetailView.as_view(), name='service_equipment_detail'),


    path('<str:slug>/equipment_address/api/', EquipmentAddressViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('<str:slug>/equipment_address/api/<int:pk>/', EquipmentAddressViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('<str:slug>/equipment_address/<int:pk>/', EquipmentAddressDetailView.as_view(), name='equipment_address_detail'),

]
