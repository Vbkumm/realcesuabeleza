from django.urls import path
from .views import (ProfessionalViewSet,
                    ProfessionalDetailView,
                    ProfessionalCategoryViewSet,
                    ProfessionalCategoryDetailView,
                    ProfessionalCategoryCreateView,
                    ProfessionalWizardCreateView,
                    ProfessionalSelectCategoryUpdateView,
                    ProfessionalCategoryUpdateServicesCategoryView)


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
    path('<str:slug>/professional/', ProfessionalWizardCreateView.as_view(), name='professional_wizard_create'),
    path(r'<str:slug>/professional_select_category/<str:professional_slug>/', ProfessionalSelectCategoryUpdateView.as_view(), name='professional_select_category_update'),
    path('<str:slug>/professional/<str:professional_slug>/', ProfessionalDetailView.as_view(), name='professional_detail'),
    path('<str:slug>/professional_category/', ProfessionalCategoryCreateView.as_view(), name='professional_category_create'),
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
    path('<str:slug>/professional_category/<str:professional_category_slug>/professional_category_update_services_category/', ProfessionalCategoryUpdateServicesCategoryView.as_view(), name='professional_category_update_services_category'),

]

