from django.urls import path
from .views import (ProfessionalViewSet,
                    ProfessionalDetailView,
                    ProfessionalCategoryViewSet,
                    ProfessionalCategoryDetailView)


urlpatterns = [
    path('<str:slug>/professional/api/', ProfessionalViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('<str:slug>/professional/api/<str:professional_slug>/', ProfessionalViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('<str:slug>/professional/<str:professional_slug>/', ProfessionalDetailView.as_view(), name='professional_detail'),

    path('<str:slug>/professional_category/api/', ProfessionalCategoryViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('<str:slug>/professional_category/api/<str:professional_category_slug>/', ProfessionalCategoryViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('<str:slug>/professional_category/<str:professional_category_slug>/', ProfessionalCategoryDetailView.as_view(), name='professional_category_detail'),

]

