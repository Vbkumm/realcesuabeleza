from django.urls import path
from .views import BusinessViewSet, BusinessDetailView


urlpatterns = [
    path('api/', BusinessViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('api/<str:slug>/', BusinessViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('<str:slug>/', BusinessDetailView.as_view(), name='business_detail'),

]