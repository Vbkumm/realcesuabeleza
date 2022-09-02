"""realcesuabeleza URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from allauth.account.views import confirm_email
from main.views import home_view, TermsView, CookiesView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),
    path('', include('businesses.urls')),
    path('', include('customers.urls')),
    path('', include('professionals.urls')),
    path('', include('services.urls')),
    path('', include('prices.urls')),
    path('terms/', TermsView.as_view(), name="terms"),
    path('cookies/', CookiesView.as_view(), name="cookies"),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts-rest/registration/account-confirm-email/(<key>.+)/', confirm_email, name='account_confirm_email'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
