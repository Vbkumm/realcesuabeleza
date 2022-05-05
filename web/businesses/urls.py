from django.urls import path
from .views import BusinessViewSet, BusinessDetailView


urlpatterns = [
    path('business_api/', BusinessViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('business_api/<str:slug>', BusinessViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('<slug>/', BusinessDetailView.as_view(), name='business_detail'),

]