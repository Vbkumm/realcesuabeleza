from django.urls import path
from .views import PriceServiceUpdateView

app_name = 'prices'


urlpatterns = [
    path(r'<str:slug>/service/<str:service_slug>/price_service_update/<int:pk>/', PriceServiceUpdateView.as_view(), name='price_service_update'),

]