from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import perform_login
from django.utils.http import url_has_allowed_host_and_scheme
from django.shortcuts import redirect
from allauth.account.adapter import DefaultAccountAdapter
from accounts.models import CustomUserModel
from realcesuabeleza import settings


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

