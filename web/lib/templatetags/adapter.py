from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import perform_login
from django.shortcuts import reverse
from allauth.account.adapter import DefaultAccountAdapter
from accounts.models import CustomUserModel
from realcesuabeleza import settings
from businesses.models import BusinessModel


class MyAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        user = super(MyAccountAdapter, self).save_user(request, user, form, commit=False)
        user.business = request.session.get("business_slug", None)
        user.save()

    def get_login_redirect_url(self, request):
        if request.session.get("business_slug", None):
            slug = request.session.get("business_slug", None)
            path = "/{slug}/"
            BusinessModel.objects.get_new_business_user(request.user, slug)
            return path.format(slug=slug)
        else:
            return settings.LOGIN_REDIRECT_URL

    def get_logout_redirect_url(self, request):

        if request.session.get("business_slug", None):
            slug = request.session.get("business_slug", None)
            path = "/{slug}/"

            return path.format(slug=slug)
        else:
            return settings.ACCOUNT_LOGOUT_REDIRECT_URL

    def get_email_confirmation_redirect_url(self, request):
        pass

    def get_signup_redirect_url(self, request):

        if request.session.get("business_slug", None):
            slug = request.session.get("business_slug", None)
            path = "/{slug}/"

            return path.format(slug=slug)
        else:
            return settings.LOGIN_REDIRECT_URL


class MySocialAccountAdapter(DefaultSocialAccountAdapter):

    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user
        if user.id:
            return
        try:
            custom_user = CustomUserModel.objects.get(email=user.email)  # if user exists, connect the account to the existing account and login
            sociallogin.state['process'] = 'connect'
            perform_login(request, custom_user, 'none')
        except CustomUserModel.DoesNotExist:
            pass

