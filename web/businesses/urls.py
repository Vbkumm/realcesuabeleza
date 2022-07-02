from django.urls import path
from .views import (BusinessViewSet,
                    BusinessDetailView,
                    user_business_add,
                    BusinessAddressDetailView,
                    BusinessWizardCreateView,
                    BusinessAddressWizardCreateView,
                    BusinessPhoneCreateView,
                    BusinessLogoQrcodeCreateView,
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
    path('business_create/', BusinessWizardCreateView.as_view(), name='business_create'),
    path('<str:slug>/', BusinessDetailView.as_view(), name='business_detail'),
    path('<str:slug>/user_business_add/', user_business_add, name='user_business_add'),
    path('<str:slug>/business_address_create/', BusinessAddressWizardCreateView.as_view(), name='business_address_create'),
    path('<str:slug>/address/<int:pk>', BusinessAddressDetailView.as_view(), name='business_address_detail'),
    path('<str:slug>/address/<int:pk>/business_phone_create/', BusinessPhoneCreateView.as_view(), name='business_phone_create'),
    path('<str:slug>/business_logo_qrcode_create/', BusinessLogoQrcodeCreateView.as_view(), name='business_logo_qrcode_create'),
    path('<str:slug>/terms/', TermsView.as_view(), name="terms"),
    path('<str:slug>/cookies/', CookiesView.as_view(), name="cookies"),

]