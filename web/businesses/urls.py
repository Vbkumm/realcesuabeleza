from django.urls import path
from .views import (BusinessViewSet,
                    BusinessDetailView,
                    BusinessAddressDetailView,
                    )
from main.views import TermsView, CookiesView


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
    path('<str:slug>/address/<int:pk>', BusinessAddressDetailView.as_view(), name='business_address_detail'),
    path('<str:slug>/terms/', TermsView.as_view(), name="terms"),
    path('<str:slug>/cookies/', CookiesView.as_view(), name="cookies"),
]